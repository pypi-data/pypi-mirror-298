import inspect
from collections import Counter
from dataclasses import dataclass
from enum import Enum, StrEnum
from itertools import zip_longest, chain
from pathlib import Path
from queue import Queue
from random import random
from typing import (
    Tuple,
    TypeAlias,
    Self,
    Unpack,
    Literal,
    Any,
    Callable,
    Hashable,
    TypeVar,
    Dict,
    Optional,
    List,
    ClassVar,
    Set,
    Sequence,
    get_type_hints,
)

from bdmc import CloseLoopController
from colorama import Fore
from numpy import array, full, int32, equal
from numpy.random import choice
from terminaltables import SingleTable

from .exceptions import StructuralError, TokenizeError
from .logger import _logger
from ..tools.generators import NameGenerator
from ..tools.selectors import make_weighted_selector

T_EXPR = TypeVar("T_EXPR", str, list)
Expression: TypeAlias = str | int

FullPattern: TypeAlias = Tuple[int]
LRPattern: TypeAlias = Tuple[int, int]
IndividualPattern: TypeAlias = Tuple[int, int, int, int]
FullExpressionPattern: TypeAlias = str
LRExpressionPattern: TypeAlias = Tuple[Expression, Expression]
IndividualExpressionPattern: TypeAlias = Tuple[Expression, Expression, Expression, Expression]
KT = TypeVar("KT", bound=Hashable)
Context: TypeAlias = Dict[str, Any]

__PLACE_HOLDER__ = 0
__CONTROLLER_NAME__ = "con"
__MAGIC_SPLIT_CHAR__ = "$$$"


class PatternType(Enum):
    """
    Three types of control cmd
    """

    Full = 1
    LR = 2
    Individual = 4


class ArrowStyle(StrEnum):
    """
    Attributes:
        DOWN: "-->"
        LEFT: "-left->"
        RIGHT: "-right->"
        UP: "-up->"
    """

    DOWN = "-->"
    LEFT = "-left->"
    RIGHT = "-right->"
    UP = "-up->"

    @classmethod
    def new(cls, direction: "ArrowStyle" | Literal["up", "down", "left", "right"] = "down") -> Self:
        """
        Create a new ArrowStyle object.
        Args:
            direction:

        Returns:

        """

        if isinstance(direction, cls):
            return direction

        match direction:
            case "up":
                return cls.UP
            case "down":
                return cls.DOWN
            case "left":
                return cls.LEFT
            case "right":
                return cls.RIGHT
            case _:
                raise ValueError(f"Must be one of {list(cls)}, but got unknown arrow style: {direction}")


def get_function_annotations(func: Callable) -> str:
    """
    Get the function annotations of a given function.

    Args:
        func (callable): The function to get the annotations for.

    Returns:
        str: A string representation of the function annotations.
    """
    try:
        # Get the function's signature
        sig = inspect.signature(func)
    except ValueError as e:
        # Handle cases where func is not a valid function
        raise ValueError(f"Invalid function: {func}") from e

    # Get the type annotations
    type_hints = get_type_hints(func)

    # Initialize strings for parameter types and return type
    param_types = []

    for param_name, param in sig.parameters.items():
        # Check if the parameter has an annotation
        if param.annotation != inspect.Parameter.empty:
            hint = type_hints.get(param_name)
            # Convert the type hint to a string representation,
            # handling complex hints like List[int] properly
            param_type_str = convert_type_str(hint)
            param_types.append(param_type_str)
        else:
            # Use 'Any' for parameters without annotations
            param_types.append("Any")

    # Handle the return type
    return_type = convert_type_str(type_hints.get("return", Any))

    # Concatenate the parameter type strings and return type to form the annotation string
    params_str = ", ".join(param_types)
    return f"def {func.__name__}({params_str}) -> {return_type}"


def convert_type_str(hint) -> str:
    """
    Convert a type hint to a string representation, handling complex types and generics.

    Args:
        hint: The type hint to convert.

    Returns:
        str: The string representation of the type hint.
    """
    if hint == type(None):
        return "None"
    elif hint in {int, float, bool, str, list, tuple, set, dict}:
        return hint.__name__
    else:
        # For other types, convert directly to string
        return str(hint).replace("typing.", "")


def bold(string: str) -> str:
    """
    Takes a string as input and returns the same string surrounded by double asterisks.

    Parameters:
        string (str): The string to be formatted.

    Returns:
        str: The input string surrounded by double asterisks.
    """
    return f"**{string}**"


class MovingState:
    """
    Describes the movement state of the bot.
    Include:
    - halt: make a stop state,all wheels stop moving
    - straight: make a straight moving state,all wheels move in the same direction,same speed
    - turn: make a turning state,left and right wheels turn in different direction,same speed
    - differential: make a differential state,all wheels move in the same direction,different speed
    - drift: make a drift state,all wheels except for a specific one drift in the same direction, specific speed

    """

    @dataclass
    class Config:
        """
        Configuration for the MovingState class.
        Args:
            track_width(int):The width of the track(AKA the distance between the wheels with a same axis). dimensionless number
            diagonal_multiplier(float):The multiplier for the diagonal speeds. dimensionless number.All designed for the drift movement.
        """

        track_width: int = 100
        diagonal_multiplier: float = 1.53

    __state_id_counter__: ClassVar[int] = 0

    @property
    def pattern_type(self) -> PatternType:
        """
        Returns the pattern type of the state.

        Returns:
            PatternType: The pattern type of the state.
        """
        return self._pattern_type

    @property
    def state_id(self) -> int:
        """
        Returns the state identifier.

        Returns:
            int: The state identifier.
        """
        return self._state_id

    @property
    def label(self) -> str:
        """unique label"""

        return f'{self._state_id}_MovingState'

    @property
    def before_entering(self) -> Optional[List[Callable[[], Any]]]:
        """
        Returns the list of functions to be called before entering the state.

        :return: An optional list of callables that take no arguments and return None.
        :rtype: Optional[List[Callable[[], None|Any]]]
        """
        return self._before_entering

    @property
    def after_exiting(self) -> Optional[List[Callable[[], Any]]]:
        """
        Returns the list of functions to be called after exiting the state.

        :return: An optional list of callables that take no arguments and return None.
        :rtype: Optional[List[Callable[[], None|Any]]]
        """
        return self._after_exiting

    @property
    def used_context_variables(self) -> List[str]:
        """
        Returns the set of context variable names used in the speed expressions.

        :return: An optional set of strings representing the context variable names.
        :rtype: Optional[List[str]]
        """
        return self._used_context_variables

    @property
    def speed_expressions(self) -> IndividualExpressionPattern:
        """
        Get the speed expressions of the object.

        :return: The speed expressions of the object.
        :rtype: IndividualExpressionPattern
        """
        return self._speed_expressions

    def __init__(
            self,
            *speeds: Unpack[FullPattern] | Unpack[LRPattern] | Unpack[IndividualPattern],
            speed_expressions: Optional[
                FullExpressionPattern | LRExpressionPattern | IndividualExpressionPattern] = None,
            used_context_variables: Optional[List[str]] = None,
            before_entering: Optional[List[Callable[[], Any]]] = None,
            after_exiting: Optional[List[Callable[[], None] | Any]] = None,
    ) -> None:
        """
        Initialize the MovingState with speeds.

        Args:
            *speeds: A tuple representing the speed pattern.
                It should be one of the following types:
                    - FullPattern: A single integer representing full speed for all directions.
                    - LRPattern: A tuple of two integers representing left and right speeds.
                    - IndividualPattern: A tuple of four integers representing individual speeds for each direction.

        Keyword Args:
            speed_expressions (Optional[FullExpressionPattern | Unpack[LRExpressionPattern] | Unpack[IndividualExpressionPattern]]): The speed expressions of the wheels.
            used_context_variables (Optional[List[str]]): The set of context variable names used in the speed expressions.
            before_entering (Optional[List[Callable[[], None|Any]]]): The list of functions to be called before entering the state.
            after_exiting (Optional[List[Callable[[], None|Any]]]]): The list of functions to be called after exiting the state.
        Raises:
            ValueError: If the provided speeds do not match any of the above patterns.
        """
        self._speed_expressions: IndividualExpressionPattern
        self._speeds: array
        self._pattern_type: PatternType
        match bool(speed_expressions), bool(speeds):
            case True, False:
                if used_context_variables is None:
                    raise ValueError(
                        "No used_context_variables provided, You must provide a names set that contains all the "
                        "name of the variables used in the speed_expressions."
                        "If you do not need use context variables, "
                        "then you should use *speeds argument to create the MovingState."
                    )
                self._speeds = None
                match speed_expressions:
                    case str(full_expression):
                        self._pattern_type = PatternType.Full
                        self._speed_expressions = (full_expression, full_expression, full_expression, full_expression)
                    case (left_expression, right_expression):
                        if all(isinstance(item, int) for item in speed_expressions):
                            raise ValueError(
                                f"All expressions are integers. You should use *speeds argument to create the MovingState, got {speed_expressions}"
                            )
                        self._pattern_type = PatternType.LR
                        self._speed_expressions = (left_expression, left_expression, right_expression, right_expression)
                    case speed_expressions if len(speed_expressions) == 4:
                        if all(isinstance(item, int) for item in speed_expressions):
                            raise ValueError(
                                f"All expressions are integers. You should use *speeds argument to create the MovingState, got {speed_expressions}"
                            )
                        self._pattern_type = PatternType.Individual
                        self._speed_expressions = speed_expressions
                    case _:
                        types = tuple(type(item) for item in speed_expressions)
                        raise ValueError(
                            f"Invalid Speed Expressions. Must be one of [{FullExpressionPattern},{LRExpressionPattern},{IndividualExpressionPattern}], got {types}"
                        )

            case False, True:
                self._speed_expressions = None
                match speeds:
                    case (int(full_speed), ):
                        self._pattern_type = PatternType.Full
                        self._speeds = full((4,), full_speed)
                    case (int(left_speed), int(right_speed)):
                        self._pattern_type = PatternType.LR

                        self._speeds = array([left_speed, left_speed, right_speed, right_speed])
                    case speeds if len(speeds) == 4 and all(isinstance(item, int) for item in speeds):
                        self._pattern_type = PatternType.Individual

                        self._speeds = array(speeds)
                    case _:
                        types = tuple(type(item) for item in speeds)
                        raise ValueError(
                            f"Invalid Speeds. Must be one of [{FullPattern},{LRPattern},{IndividualPattern}], got {types}"
                        )
            case True, True:
                raise ValueError(
                    f"Cannot provide both speeds and speed_expressions, got {speeds} and {speed_expressions}"
                )

            case False, False:
                raise ValueError(
                    f"Must provide either speeds or speed_expressions, got {speeds} and {speed_expressions}"
                )

        if used_context_variables:
            self._validate_used_context_variables(used_context_variables, self._speed_expressions)
        self._used_context_variables: List[str] = used_context_variables or []
        self._before_entering: List[Callable[[], Any]] = before_entering or []
        self._after_exiting: List[Callable[[], Any]] = after_exiting or []
        self._state_id: int = MovingState.__state_id_counter__
        MovingState.__state_id_counter__ += 1

    @staticmethod
    def _validate_used_context_variables(
            used_context_variables: List[str], speed_expressions: IndividualExpressionPattern
    ) -> None:
        if len(used_context_variables) != len(set(used_context_variables)):
            raise ValueError(f"used_context_variables can't contain duplicated item!")
        for variable in used_context_variables:
            if any(variable in str(expression) for expression in speed_expressions):
                continue
            raise ValueError(f"Variable {variable} not found in {speed_expressions}.")

    @classmethod
    def rand_move(
            cls,
            con: CloseLoopController,
            speeds: Sequence[Tuple[int, int, int, int]],
            weights: Optional[Sequence[float | int]] = None,
            used_ctx_varname: str = "rand_move",
    ) -> Self:
        """
        Registers a random movement behavior with the given CloseLoopController.

        This method randomly selects a speed tuple from the provided list and updates the turn direction
        before entering the behavior. If weights are provided, the selection is made according to them.

        Args:
            con: CloseLoopController instance to register the behavior with.
            speeds: A sequence of speed tuples, each representing velocities for four directions.
            weights: Optional sequence of weights corresponding to the speeds. If given, the selection is weighted.
            used_ctx_varname: str, the name of the context variable to store the selected speed.

        Returns:
            Self: An instance of the class with the random move behavior configured.
        """
        if weights and len(weights) != len(speeds):
            raise ValueError(f"weights and speeds must have the same length, got speeds: {speeds}, weights: {weights}.")
        indexes = tuple(range(len(speeds)))

        # Register a context updater to update the turn direction before entering the behavior.
        _updater = con.register_context_executor(
            make_weighted_selector(speeds, weights) if weights else lambda: speeds[choice(indexes)],
            output_keys=[used_ctx_varname],
            function_name=f"update_{used_ctx_varname}",
        )

        # Configure speed expressions and actions before entering, implementing random turning.
        return cls(
            speed_expressions=(
                f"{used_ctx_varname}[0]",
                f"{used_ctx_varname}[1]",
                f"{used_ctx_varname}[2]",
                f"{used_ctx_varname}[3]",
            ),
            used_context_variables=[used_ctx_varname],
            before_entering=[_updater],
        )

    @classmethod
    def halt(cls) -> Self:
        """
        Create a new instance of the class with a speed of 0, effectively halting the movement.

        Returns:
            Self: A new instance of the class with a speed of 0.
        """
        return cls(0)

    @classmethod
    def straight(cls, speed: int) -> Self:
        """
        Create a new instance of the class with the specified speed.
        Lets the bot drive straight with the specified speed.

        Args:
            speed (int): The speed value to be used for the new instance. Positive for forward and negative for backward.

        Returns:
            Self: A new instance of the class with the specified speed.
        """
        return cls(speed)

    @classmethod
    def rand_spd_straight(
            cls,
            con: CloseLoopController,
            speeds: Sequence[int],
            weights: Optional[Sequence[float | int]] = None,
            used_ctx_varname: str = "rand_speed",
    ) -> Self:
        """
        Create a new instance of the class with a random speed.
        Args:
            con (CloseLoopController): CloseLoopController object, representing the instance to which the random turning control is applied.
            speeds (Sequence[int]): A sequence of speeds.
            weights (Optional[Sequence[float | int]]): Weights for each speed.
            used_ctx_varname (str, optional): The name of the context variable to store the selected speed.

        Returns:

        """
        if weights and len(weights) != len(speeds):
            raise ValueError(f"weights and speeds must have the same length, got speeds: {speeds}, weights: {weights}.")
        # Register a context updater to update the turn direction before entering this behavior.
        _updater = con.register_context_executor(
            make_weighted_selector(speeds, weights) if weights else lambda: choice(speeds),
            output_keys=[used_ctx_varname],
            function_name=f"update_{used_ctx_varname}",
        )

        # Set speed expressions and actions before entering, implementing random turning.
        return cls(
            speed_expressions=used_ctx_varname,
            used_context_variables=[used_ctx_varname],
            before_entering=[_updater],
        )

    @classmethod
    def differential(cls, direction: Literal["l", "r"], radius: float, outer_speed: int) -> Self:
        """
        Create a new instance of the class with the specified differential movement.
        Let the bot make a differential movement with the specified radius and speed.

        Note:
            The outer speed is the speed of the outer wheel.
            The unit of the radius is a dimensionless number, not CM, not MM, etc.
            The inner speed is calculated from the outer speed and the radius and the track_width.
        Args:
            direction (Literal["l", "r"]): The direction of the movement. Must be one of "l" or "r".
            radius (float): The radius of the movement.
            outer_speed (int): The speed of the outer wheel.

        Returns:
            Self: A new instance of the class with the specified differential movement.

        Raises:
            ValueError: If the direction is not one of "l" or "r".

        """
        inner_speed = int(radius / (radius + cls.Config.track_width) * outer_speed)

        match direction:
            case "l":
                return cls(inner_speed, outer_speed)
            case "r":
                return cls(outer_speed, inner_speed)
            case _:
                raise ValueError("Invalid Direction. Must be one of ['l','r']")

    @classmethod
    def turn(cls, direction: Literal["l", "r"], speed: int) -> Self:
        """
        Create a new instance of the class with the specified turn direction and speed.
        Lets the bot make a turn with the specified direction and speed in place.

        Args:
            direction (Literal["l", "r"]): The direction of the turn. Must be one of "l" or "r".
            speed (int): The speed of the turn.

        Returns:
            Self: A new instance of the class with the specified turn direction and speed.

        Raises:
            ValueError: If the direction is not one of "l" or "r".
        """
        match direction:
            case "l":
                return cls(-speed, speed)
            case "r":
                return cls(speed, -speed)
            case _:
                raise ValueError("Invalid Direction. Must be one of ['l','r']")

    @classmethod
    def rand_dir_turn(
            cls,
            con: CloseLoopController,
            turn_speed: int,
            turn_left_prob: float = 0.5,
            used_ctx_varname: str = "rand_direction",
    ) -> Self:
        """
        Adds a method for random turning to the CloseLoopController class.

        Parameters:
            cls: Class method convention parameter, referring to the current class.
            con: CloseLoopController object, representing the instance to which the random turning control is applied.
            turn_speed: Turning speed, positive for turning right, negative for turning left.
            used_ctx_varname: Context variable name used to represent the turn direction, defaults to "direction".
            turn_left_prob: Probability of turning left, defaults to 0.5, meaning equal chance of turning left or right.

        Returns:
            Self: A new instance of the class with a random turn direction and speed.
        """
        if turn_speed < 0:
            _logger.warn(
                f"Turn speed must be positive, got {turn_speed}, "
                f"if you 'd like to turn right, lower the value of turn_left_prob instead."
            )

        def _dir() -> int:
            """
            Internal function to randomly decide the turn direction.

            Returns:
                int: 1 for turning left, -1 for turning right.
            """
            return 1 if random() < turn_left_prob else -1

        # Register a context updater to update the turn direction before entering this behavior.
        _updater = con.register_context_executor(
            _dir, output_keys=[used_ctx_varname], function_name=f"update_{used_ctx_varname}"
        )

        # Set speed expressions and actions before entering, implementing random turning.
        return cls(
            speed_expressions=(f"{-turn_speed}*{used_ctx_varname}", f"{turn_speed}*{used_ctx_varname}"),
            used_context_variables=[used_ctx_varname],
            before_entering=[_updater],
        )

    @classmethod
    def rand_spd_turn(
            cls,
            con: CloseLoopController,
            direction: Literal["l", "r"],
            turn_speeds: Sequence[int],
            weights: Optional[Sequence[float | int]] = None,
            used_ctx_varname: str = "rand_speed",
    ) -> Self:
        """
        Generates a random turning behavior for a CloseLoopController.

        Parameters:
            cls: Class method convention parameter, referring to the current class.
            con: The CloseLoopController object to apply the random turning behavior to.
            direction: Turning direction, either "l" (left) or "r" (right).
            turn_speeds: A sequence of turning speeds to randomly select from.
            weights: An optional sequence of weights corresponding to turn_speeds for weighted selection.
            used_ctx_varname: The variable name to use in the context to store the selected turning speed. Default is "rand_speed".

        Returns:
            Self: An instance of the class configured with the random turning behavior.
        """
        if any(num < 0 for num in turn_speeds):
            _logger.warn(
                f"All turn speeds should be positive, got {turn_speeds}. "
                f"Since you should not using the turn left with negative speed to represent turn right."
            )

        match direction:
            case "l":
                direction = 1
            case "r":
                direction = -1
            case _:
                raise ValueError("Invalid Direction. Must be one of ['l','r']")
        _spd = make_weighted_selector(turn_speeds, weights) if weights else lambda: choice(turn_speeds)

        # Register a context updater to update the turn direction before entering this behavior.

        _updater = con.register_context_executor(
            _spd, output_keys=[used_ctx_varname], function_name=f"update_{used_ctx_varname}"
        )

        # Set speed expressions and actions before entering, implementing random turning.

        return cls(
            speed_expressions=(f"{-direction}*{used_ctx_varname}", f"{direction}*{used_ctx_varname}"),
            used_context_variables=[used_ctx_varname],
            before_entering=[_updater],
        )

    @classmethod
    def rand_dir_spd_turn(
            cls,
            con: CloseLoopController,
            turn_speeds: Sequence[int],
            weights: Optional[Sequence[float | int]] = None,
            used_ctx_varname: str = "rand_dir_speed",
    ) -> Self:
        """
        Generates an instance of CloseLoopController that randomly selects a turning speed before entering the behavior.
        It updates the context variable with the chosen speed.

        Args:
            con (CloseLoopController): The controller instance to modify.
            turn_speeds (Sequence[int]): A sequence of turning speeds. positive means turn left, negative means turn right
            weights (Optional[Sequence[float | int]], optional): Weights for each turning speed. If provided, speeds will be selected probabilistically. Defaults to None.
            used_ctx_varname (str, optional): The name of the context variable to store the selected speed. Defaults to "rand_dir_speed".

        Returns:
            Self: An instance of the CloseLoopController class with the configured random turning behavior.
        """
        # Warn if all turn speeds have the same sign, suggesting the use of rand_spd_turn instead.
        if all(num > 0 for num in turn_speeds) or all(num < 0 for num in turn_speeds):
            _logger.warn("All speeds have the same sign, consider using rand_spd_turn")

        # Select a turning speed based on given weights or randomly.
        _spd = make_weighted_selector(turn_speeds, weights) if weights else lambda: choice(turn_speeds)

        # Register a context updater to update the turn direction before entering this behavior.
        _updater = con.register_context_executor(
            _spd, output_keys=[used_ctx_varname], function_name=f"update_{used_ctx_varname}"
        )

        # Set speed expressions and actions before entering, implementing random turning.
        return cls(
            speed_expressions=(f"-{used_ctx_varname}", f"{used_ctx_varname}"),
            used_context_variables=[used_ctx_varname],
            before_entering=[_updater],
        )

    @classmethod
    def drift(cls, fixed_axis: Literal["fl", "rl", "rr", "fr"], speed: int) -> Self:
        """
        Create a new instance of the class with the specified drift direction and speed.
        Lets the bot make a drift with the specified direction and speed in place.

        Note:
            This movement is achieved by making a wheel fixed, while the others move with the specified speed.

            The drift movement is affected by the Config.diagonal_multiplier.


        Args:
            fixed_axis (Literal["fl", "rl", "rr", "fr"]): The direction of the drift. Must be one of "fl", "rl", "rr", or "fr".
            speed (int): The speed of the drift.

        Returns:
            Self: A new instance of the class with the specified drift direction and speed.

        Raises:
            ValueError: If the axis is not one of "fl", "rl", "rr", or "fr".
        """
        match fixed_axis:
            case "fl":
                return cls(0, speed, int(speed * cls.Config.diagonal_multiplier), speed)
            case "rl":
                return cls(speed, 0, speed, int(speed * cls.Config.diagonal_multiplier))
            case "rr":
                return cls(int(speed * cls.Config.diagonal_multiplier), speed, 0, speed)
            case "fr":
                return cls(speed, int(speed * cls.Config.diagonal_multiplier), speed, 0)
            case _:
                raise ValueError("Invalid Direction. Must be one of ['fl','rl','rr','fr']")

    def apply(self, multiplier: float) -> Self:
        """
        Apply a multiplier to the speeds of the object and return the modified object.

        Args:
            multiplier (float): The multiplier to apply to the speeds.

        Returns:
            Self: The modified object with the updated speeds.
        """
        self._speeds = (self._speeds * multiplier).astype(int32)
        return self

    def unwrap(self) -> Tuple[int, ...]:
        """
        Return the speeds of the MovingState object.
        """
        if self._speeds is None:
            raise "The Speeds is not defined! You can not unwrap!"

        return tuple(self._speeds.tolist())

    def clone(self) -> Self:
        """
        Creates a clone of the current `MovingState` object.

        Returns:
            Self: A new `MovingState` object with the same speeds as the current object.
        """
        if self._speeds is not None:

            return MovingState(
                *self.unwrap(),
                before_entering=list(self._before_entering),
                after_exiting=list(self._after_exiting),
            )
        else:
            return MovingState(
                speed_expressions=self._speed_expressions,
                used_context_variables=list(self._used_context_variables),
                before_entering=list(self._before_entering),
                after_exiting=list(self._after_exiting),
            )

    def tokenize(self, con: Optional[CloseLoopController]) -> Tuple[List[str], Context]:
        """
        Converts the current state into a list of tokens and a context dictionary.

        Parameters:
        - con: Optional[CloseLoopController] - The closed-loop controller required if speed expressions exist.

        Returns:
        - Tuple[List[str], Context]: A tuple containing the list of tokens and the context dictionary.

        Raises:
        - TokenizeError: If the state contains both speeds and speed expressions, or neither.
        - RuntimeError: If an internal logic error occurs; this state should理论上 never be reached.
        """

        # Check for simultaneous presence or absence of speeds and speed expressions

        if self._speeds is not None and self._speed_expressions:
            raise TokenizeError(
                f"Cannot tokenize a state with both speed expressions and speeds, got {self.unwrap()} and {self._speed_expressions}."
            )
        elif self._speeds is None and self._speed_expressions is None:
            raise TokenizeError(f"Cannot tokenize a state with no speed expressions and no speeds.")

        context: Context = {}  # Initialize the context dictionary
        context_updater_func_name_generator: NameGenerator = NameGenerator(f"state{self._state_id}_context_updater_")

        # Generate tokens for actions before entering the state
        before_enter_tokens: List[str] = []
        if self._before_entering:
            for func in self._before_entering:
                context[(func_var_name := context_updater_func_name_generator())] = func
                before_enter_tokens.append(f".wait_exec({func_var_name})")

        # Generate tokens for actions after exiting the state
        after_exiting_tokens: List[str] = []
        if self._after_exiting:
            for func in self._after_exiting:
                context[(func_var_name := context_updater_func_name_generator())] = func
                after_exiting_tokens.append(f".wait_exec({func_var_name})")

        state_tokens: List[str] = []
        # Generate tokens based on speed expressions or speeds
        match self._speed_expressions, self._speeds:
            case expression, None:
                if con is None:
                    raise TokenizeError(
                        f"You must parse a CloseLoopController to tokenize a state with expression pattern"
                    )

                getter_function_name_generator = NameGenerator(f"state{self._state_id}_context_getter_")
                getter_temp_name_generator = NameGenerator(f"state{self._state_id}_context_getter_temp_")

                # this is to avoid re-calc in Full pattern and LR pattern
                expression_final_value_temp = NameGenerator(f"state{self._state_id}_val_tmp")

                match self._pattern_type:
                    case PatternType.Full:
                        expression: Tuple[str, str, str, str]
                        input_arg_string = self._make_arg_string_full_pattern(
                            con,
                            context,
                            expression,
                            expression_final_value_temp,
                            getter_function_name_generator,
                            getter_temp_name_generator,
                        )
                    case PatternType.LR:
                        expression: IndividualExpressionPattern
                        input_arg_string = self._make_arg_string_lr_pattern(
                            con,
                            context,
                            expression,
                            expression_final_value_temp,
                            getter_function_name_generator,
                            getter_temp_name_generator,
                        )

                    case PatternType.Individual:
                        input_arg_string = self._make_arg_string_single_pattern(
                            con, context, expression, getter_function_name_generator, getter_temp_name_generator
                        )
                    case _:
                        raise TokenizeError(f"Unknown expression type, got {self._pattern_type}")
                state_tokens.append(f".set_motors_speed({input_arg_string})")

            case None, speeds if speeds is not None:
                state_tokens.append(f".set_motors_speed({self.unwrap()})")
            case _:
                raise TokenizeError("should never reach here")

        tokens: List[str] = before_enter_tokens + state_tokens + after_exiting_tokens
        return tokens, context

    def _make_arg_string_single_pattern(
            self,
            con: CloseLoopController,
            context: Context,
            expression: IndividualExpressionPattern,
            getter_function_name_generator: NameGenerator,
            getter_temp_name_generator: NameGenerator,
    ) -> str:
        """
        Generates a parameter string for a single expression pattern.

        Args:
            con: An instance of CloseLoopController used to register context getters.
            context: An instance of Context used to store generated context getter functions.
            expression: An instance of IndividualExpressionPattern representing a single expression pattern.
            getter_function_name_generator: An instance of NameGenerator used to generate names for context getter functions.
            getter_temp_name_generator: An instance of NameGenerator used to generate temporary variable names.

        Returns:
            str: A generated parameter string where variables in the expression are replaced with calls to corresponding context getter functions.
        """
        # Initialize the argument string by converting the expression to a tuple's string representation and removing quotes.
        input_arg_string: str = str(tuple(expression)).replace("'", "")
        # Iterate over the context variables used to generate the expressions.
        for varname in self._used_context_variables:

            # Register a context getter that takes the variable name and returns a callable object.
            fn: Callable[[], Any] = con.register_context_getter(varname)
            # Store this getter function in the context using the generated function name.
            context[(getter_func_var_name := getter_function_name_generator())] = fn
            # Generate a temporary variable name for referencing context values in the argument string.
            temp_name = getter_temp_name_generator()

            # If the variable name appears only once in the argument string, replace it directly with a function call.
            if input_arg_string.count(varname) == 1:
                input_arg_string = input_arg_string.replace(varname, f"{getter_func_var_name}()", 1)
            else:
                # If the variable name appears multiple times, replace the first occurrence with an assignment-based function call, and subsequent occurrences with the temporary variable name.
                input_arg_string = input_arg_string.replace(varname, f"({temp_name}:={getter_func_var_name}())", 1)
                input_arg_string = input_arg_string.replace(varname, temp_name)
        # Return the final generated argument string.
        return input_arg_string

    def _make_arg_string_lr_pattern(
            self,
            con: CloseLoopController,
            context: Context,
            expression: IndividualExpressionPattern,
            expression_final_value_temp: NameGenerator,
            getter_function_name_generator: NameGenerator,
            getter_temp_name_generator: NameGenerator,
    ) -> str:
        """
        Constructs a parameter string for left and right expressions.

        Args:
            con: An instance of the closed-loop controller to register context getters.
            context: The context environment to store generated getter functions.
            expression: An expression pattern containing two expressions (left and right).
            expression_final_value_temp: A generator for creating temporary variable names for final expression values.
            getter_function_name_generator: A generator for creating names for context getter functions.
            getter_temp_name_generator: A generator for creating temporary variable names for context getter functions.

        Returns:
            A constructed parameter string for further operations.

        Raises:
            TokenizeError: If both parts of the expression are integers, an exception is raised.
            RuntimeError: If an unexpected situation occurs, an exception is raised.
        """
        # Generate temporary variable names for storing the final value of the expressions
        l_val_temp_name: str = expression_final_value_temp()
        r_val_temp_name: str = expression_final_value_temp()
        # Build a combined string of left and right expressions
        lr_expression: str = f"{expression[0]}{__MAGIC_SPLIT_CHAR__}{expression[-1]}"
        # Iterate over used context variables, create context getter functions, and replace variables in expressions
        for varname in self._used_context_variables:
            fn: Callable[[], Any] = con.register_context_getter(varname)
            context[getter_func_var_name := getter_function_name_generator()] = fn
            lr_expression = self._replace_var(
                lr_expression, varname, getter_func_var_name, getter_temp_name_generator()
            )
        # Split the left and right expressions
        left_expression, right_expression = lr_expression.split(__MAGIC_SPLIT_CHAR__)
        # Based on the types of the left and right expressions, construct different parameter strings
        match isinstance(expression[0], int), isinstance(expression[-1], int):
            case True, True:
                raise TokenizeError(f"Should never be here!")
            case False, False:
                input_arg_string = f"({l_val_temp_name}:=({left_expression}),{l_val_temp_name},{r_val_temp_name}:=({right_expression}),{r_val_temp_name})"
            case False, True:
                input_arg_string = (
                    f"({l_val_temp_name}:=({left_expression}),{l_val_temp_name},{right_expression},{right_expression})"
                )
            case True, False:
                input_arg_string = (
                    f"({left_expression},{left_expression},{r_val_temp_name}:=({right_expression}),{r_val_temp_name})"
                )
            case _:
                raise RuntimeError("Should never arrive here!")
        return input_arg_string

    def _make_arg_string_full_pattern(
            self,
            con: CloseLoopController,
            context: Context,
            expression: Tuple[str, str, str, str],
            expression_final_value_temp: NameGenerator,
            getter_function_name_generator: NameGenerator,
            getter_temp_name_generator: NameGenerator,
    ) -> str:
        """
        Constructs a full argument string pattern.

        Args:
            con: An instance of CloseLoopController used to get context variables.
            context: A dictionary storing context variables and getter functions.
            expression: A tuple containing parts of the expression to build the final expression.
            expression_final_value_temp: A generator for creating temporary variable names for the final value of the expression.
            getter_function_name_generator: A generator for creating names for context getter functions.
            getter_temp_name_generator: A generator for creating temporary variable names for getter function calls.

        Returns:
            The constructed argument string pattern.
        """
        # Generate a temporary variable name for storing the final value of the expression
        val_temp_name: str = expression_final_value_temp()
        # Initialize the full expression with the first element of the tuple
        full_expression = expression[0]

        # Iterate over all used context variables, create a getter function for each, and replace variable names in the expression
        for varname in self._used_context_variables:
            # Create a context getter function using an expression
            fn: Callable[[], Any] = con.register_context_getter(varname)
            # Generate a name for the getter function and store it in the context
            context[getter_func_var_name := getter_function_name_generator()] = fn
            # Replace variable names in the expression with getter function calls
            full_expression = self._replace_var(
                full_expression, varname, getter_func_var_name, getter_temp_name_generator()
            )

        # Construct the final argument string pattern
        input_arg_string = f"({val_temp_name}:=({full_expression}),{val_temp_name},{val_temp_name},{val_temp_name})"
        return input_arg_string

    @staticmethod
    def _replace_var(source: str, var_name: str, func_name: str, temp_name: str) -> str:
        if source.count(var_name) == 1:
            return source.replace(var_name, f"{func_name}()", 1)
        else:
            return source.replace(var_name, f"({temp_name}:={func_name}())", 1).replace(var_name, temp_name)

    def __hash__(self) -> int:
        return self._state_id

    def __eq__(self, other: Self) -> bool:
        if self._speeds is None or other._speeds is None:
            return self._speed_expressions == other._speed_expressions
        elif self._speeds is None:
            return False
        elif other._speeds is None:
            return False
        else:

            return all(equal(self._speeds, other._speeds)) and self._speed_expressions == other._speed_expressions

    def __str__(self):
        main_seq = self._speed_expressions if self._speeds is None else self.unwrap()
        if all(main_seq[0] == x for x in main_seq[1:]):
            return f"{self._state_id}-MovingState({repr(main_seq[0])})"
        if main_seq[0] == main_seq[1] != main_seq[-1] == main_seq[-2]:
            return f"{self._state_id}-MovingState{main_seq[1:3]}"
        return f"{self._state_id}-MovingState{main_seq}"

    def __repr__(self):
        return str(self)


class MovingTransition:
    """
    A class that represents a moving transition.
    A moving transform is a transition between two states in a state machine.
    Features multiple branches and a breaker function to determine if the transition should be broken.
    """

    __transition_id_counter__: ClassVar[int] = 0

    @property
    def transition_id(self) -> int:
        """The unique identifier of the transition."""
        return self._transition_id

    @property
    def label(self) -> str:
        """unique label"""
        return f'{self._transition_id}_MovingTransition'

    def __init__(
            self,
            duration: float,
            breaker: Optional[Callable[[], KT] | Callable[[], bool] | Callable[[], Any]] = None,
            check_interval: Optional[float] = 0.01,
            from_states: Optional[Sequence[MovingState] | MovingState] = None,
            to_states: Optional[Dict[KT, MovingState] | MovingState] = None,
    ):
        """
        Initialize a MovingTransition object.

        Args:
            duration: The transition duration, must be a non-negative float.
            breaker: An optional callback function that can return a key (of type KT), a boolean, or any other value, used to interrupt the current state transition.
            check_interval: The frequency at which to check for state transition, i.e., how often in seconds to check.
            from_states: The starting states for the transition, can be a MovingState instance or a sequence of them.
            to_states: The destination states mapped to corresponding MovingState instances, or directly a MovingState instance.

        Raises:
            ValueError: If duration is negative, or from_states, to_states parameters are incorrectly formatted.
        """

        # Validate the duration
        if duration < 0:
            raise ValueError(f"Duration can't be negative, got {duration}")

        # Initialize attributes
        self.duration: float = duration
        self.breaker: Optional[Callable[[], Any]] = breaker
        self.check_interval: float = check_interval

        # Process the initial states parameter
        match from_states:
            case None:
                self.from_states: List[MovingState] = []
            case state if isinstance(state, MovingState):
                self.from_states: List[MovingState] = [from_states]
            case state if isinstance(state, Sequence) and all(isinstance(s, MovingState) for s in state):
                self.from_states: List[MovingState] = list(from_states)
            case _:
                raise ValueError(f"Invalid from_states, got {from_states}")

        # Process the target states parameter
        match to_states:
            case None:
                self.to_states: Dict[KT, MovingState] = {}
            case state if isinstance(state, MovingState):
                self.to_states: Dict[KT, MovingState] = {__PLACE_HOLDER__: state}
            case state if isinstance(state, Dict):
                self.to_states: Dict[KT, MovingState] = to_states
            case _:
                raise ValueError(f"Invalid to_states, got {to_states}")

        # Assign a unique transition ID
        self._transition_id: int = MovingTransition.__transition_id_counter__
        MovingTransition.__transition_id_counter__ += 1

    def add_from_state(self, state: MovingState) -> Self:
        """
        Adds a `MovingState` object to the `from_state` list.

        Args:
            state (MovingState): The `MovingState` object to be added.

        Returns:
            Self: The current instance of the class.
        """
        self.from_states.append(state)
        return self

    def add_to_state(self, key: KT, state: MovingState) -> Self:
        """
        Adds a state to the `to_states` dictionary with the given key and state.

        Args:
            key (KT): The key to associate with the state.
            state (MovingState): The state to add to the dictionary.

        Returns:
            Self: The current instance of the class.
        """
        self.to_states[key] = state
        return self

    def tokenize(self) -> Tuple[List[str], Context]:
        """
        Tokenizes the current object and returns a tuple of tokens and context.

        Returns:
            Tuple[List[str], Context]: A tuple containing a list of tokens and a context dictionary.
        """
        tokens: List[str] = []
        context: Context = {}
        name_generator: NameGenerator = NameGenerator(f"transition{self._transition_id}_breaker_")
        match len(self.to_states):
            case 0:
                raise TokenizeError(f"Transition must have at least one to_state, got {self.to_states}.")
            case 1 if not callable(self.breaker):
                tokens.append(f".delay({self.duration})")
            case 1 if callable(self.breaker):
                context[(breaker_name := name_generator())] = self.breaker
                tokens.append(f".delay_b({self.duration},{breaker_name},{self.check_interval})")
            case length if length > 1 and callable(self.breaker):
                context[(breaker_name := name_generator())] = self.breaker
                tokens.append(f".delay_b_match({self.duration},{breaker_name},{self.check_interval})")
            case length if length > 1 and not callable(self.breaker):
                raise TokenizeError(
                    f"got branching states {self.to_states}, but not give correct breaker, {self.breaker} is not a callable."
                )
            case _:
                raise TokenizeError(f"Undefined Error, got {self.to_states} and {self.breaker}.")
        return tokens, context

    def clone(self) -> Self:
        """
        Clones the current `MovingTransition` object and returns a new instance with the same values.

        Returns:
            Self: A new `MovingTransition` object with the same values as the current object.
        """
        return MovingTransition(
            self.duration,
            self.breaker,
            self.check_interval,
            list(self.from_states),
            dict(self.to_states),
        )

    def __eq__(self, other):
        return (
                self.duration == other.duration
                and self.breaker == other.breaker
                and self.check_interval == other.check_interval
                and self.from_states == other.from_states
                and self.to_states == other.to_states
        )

    def __str__(self):
        temp = [["From", "To"]]
        for from_state, to_state in zip_longest(self.from_states, self.to_states.values()):
            temp.append([str(from_state) if from_state else "", str(to_state) if to_state else ""])

        temp.append(
            [
                f"Duration: {self.duration:.3f}s",
                f"Breaker: {get_function_annotations(self.breaker) if callable(self.breaker) else None}",
            ]
        )
        s_table = SingleTable(temp, title=f"{self._transition_id}-MovingTransition")
        s_table.inner_footing_row_border = True
        return s_table.table

    def __repr__(self):
        return f"{self.from_states} => {list(self.to_states.values())}".replace("[", "<").replace("]", ">")

    def __hash__(self):
        return self._transition_id


TokenPool: TypeAlias = List[MovingTransition]


class Botix:
    """
    Args:
        *controller* : A `CloseLoopController` object that represents the bot's controller.
        *token_pool* : A `TokenPool` object that represents the bot's token pool.
    """

    def __init__(self, controller: CloseLoopController, token_pool: Optional[TokenPool] = None):
        self.controller: CloseLoopController = controller
        self.token_pool: TokenPool = token_pool or []

    @staticmethod
    def acquire_unique_start(token_pool: TokenPool, none_check: bool = True) -> MovingState | None:
        """
        Retrieves a unique starting state from the given token pool.

        Parameters:
        - token_pool: An instance of TokenPool, representing a collection of tokens.
        - none_check: A boolean, defaulting to True. If True, raises a ValueError when no unique starting state is found; otherwise, returns None.

        Returns:
        - Either a MovingState or None. Returns the starting state (with indegree 0) if uniquely identified; based on none_check's value, either returns None or raises an exception.
        """
        # Identifies states with an indegree of zero
        zero_indegree_states = list(states_indegree := Botix.acquire_start_states(token_pool))

        # Validates that there is exactly one state with an indegree of zero
        if len(zero_indegree_states) == 1:
            return zero_indegree_states[0]
        else:
            if none_check:
                # Raises an error if none_check is enabled and no unique starting state is present
                raise ValueError(f"There must be exactly one state with a zero indegree, got {states_indegree}")
            return None

    @staticmethod
    def acquire_start_states(token_pool: TokenPool) -> Set[MovingState]:
        """
        Calculates the starting states in the given token pool.

        Parameters:
            token_pool (TokenPool): A list of MovingTransition objects representing the token pool.

        Returns:
            Set[MovingState]: A set of MovingState objects representing the starting states in the token pool.
                The starting states are the states with an indegree of zero.

        Algorithm:
            1. Initialize a dictionary to hold the indegree of each state.
            2. Calculate the indegree for each state by examining token transitions.
            3. Identify states with an indegree of zero.
            4. Return a set of MovingState objects representing the starting states.

        Note:
            - The indegree of a state is the number of tokens that can reach that state.
            - A state is considered a starting state if it has an indegree of zero.
        """
        # Initialize a dictionary to hold the indegree of each state
        states_indegree: Dict[MovingState, int] = {}

        # Calculates the indegree for each state by examining token transitions
        for token in token_pool:
            for state in token.from_states:
                states_indegree[state] = states_indegree.get(state, 0)
            for state in token.to_states.values():
                # Increments the indegree for each state that a token can reach
                states_indegree[state] = states_indegree.get(state, 0) + 1

        # Identifies states with an indegree of zero
        zero_indegree_states = {state for state, indegree in states_indegree.items() if indegree == 0}
        return zero_indegree_states

    @staticmethod
    def acquire_end_states(token_pool: TokenPool) -> Set[MovingState]:
        """
        Calculates the end states of the given token pool.

        This function iterates through each token in the provided token pool,
        counting the number of outgoing transitions from each state.
        States with no outgoing transitions are considered end states.

        Args:
            token_pool (TokenPool): A list of MovingTransform objects representing the token pool.

        Returns:
            Set[MovingState]: A set of MovingState objects representing the end states of the token pool.
        """
        # Initialize a dictionary to keep track of the outdegree (number of outgoing transitions)
        # for each state.
        states_outdegree: Dict[MovingState, int] = {}

        # Count the number of outgoing transitions from each state.
        for token in token_pool:
            for from_state in token.from_states:
                states_outdegree[from_state] = states_outdegree.get(from_state, 0) + 1
            for to_state in token.to_states.values():
                states_outdegree[to_state] = states_outdegree.get(to_state, 0)

        # Identify end states by finding states with an outdegree of 0.
        end_states = {state for state, outdegree in states_outdegree.items() if outdegree == 0}

        return end_states

    @staticmethod
    def ensure_accessibility(token_pool: TokenPool, start_state: MovingState, end_states: Set[MovingState]) -> None:
        """
        Ensures that all states in the given token pool are accessible from the start state.

        This method performs a breadth-first search to check if all specified end states can be reached
        from the given start state by traversing through the token pool. It raises a ValueError if any
        end state is not accessible.

        Args:
            token_pool (TokenPool): A list of MovingTransform objects representing the token pool.
            start_state (MovingState): The starting state from which to check accessibility.
            end_states (Set[MovingState]): A set of MovingState objects representing the end states of the token pool.

        Raises:
            ValueError: If there are states that are not accessible from the start state.

        Returns:
            None

        Note:
            The structure validity of the token pool does not affect the accessibility check,
            So, if the token pool is not structurally valid, this method will still complete the check.
        """
        # Initialize a queue for BFS and a set to keep track of states not accessible from the start state
        search_queue: List[MovingState] = [start_state]
        not_accessible_states: Set[MovingState] = end_states
        visited_states: Set[MovingState] = set()
        # Perform breadth-first search to find if all end states are accessible
        while search_queue:
            # Pop the next state from the queue to explore
            current_state: MovingState = search_queue.pop(0)
            connected_states: Set[MovingState] = set()

            # Explore all tokens that can be reached from the current state
            for token in token_pool:
                if current_state in token.from_states:
                    # Add all to_states of the current token to the connected states list
                    connected_states.update(token.to_states.values())
            search_queue.extend((newly_visited := connected_states - visited_states))
            # Update the set of not accessible states by removing the states we just found to be connected
            not_accessible_states -= newly_visited
            visited_states.update(connected_states)
            # If there are no more not accessible states, we are done
            if len(not_accessible_states) == 0:
                return

        # If there are still states marked as not accessible, raise an exception
        if not_accessible_states:
            raise ValueError(f"States {not_accessible_states} are not accessible from {start_state}")

    @staticmethod
    def ensure_structure_validity(pool: TokenPool) -> None:
        """
        Ensures the structural validity of a given token pool by verifying that each state connects to exactly one transition as its input.
        Branching logic is implemented within the MovingTransition class.

        Parameters:
            pool (TokenPool): A list of MovingTransform objects representing the token pool.

        Raises:
            StructuralError: If any state is found connecting to multiple transitions as inputs.
                The error message includes details on the conflicting transitions for each affected state.

        Returns:
            None: If all states connect to a single input transition.
        """
        # Collect all states from the pool
        states: List[MovingState] = []

        for trans in pool:
            states.extend(trans.from_states)
        # Count occurrences of each state
        element_counts = Counter(states)

        # Identify states with multiple occurrences (potential structural issues)
        frequent_elements: List[MovingState] = [element for element, count in element_counts.items() if count >= 2]
        if not frequent_elements:
            return None
        # Construct error message
        std_err = (
            "Each state must connect to EXACTLY one transition as its input, as branching is implemented INSIDE the MovingTransition class.\n"
            "Below are error details:\n"
        )
        for state in frequent_elements:
            # Find transitions conflicting with the current state
            conflict_trans: List[MovingTransition] = list(
                filter(lambda transition: state in transition.from_states, pool)
            )
            std_err += f"For {state}, there are {len(conflict_trans)} conflicting transitions:\n\t" + "\n\t".join(
                [f"{trans}" for trans in conflict_trans]
            )
        # Raise StructuralError with the prepared message
        raise StructuralError(std_err)

    def acquire_loops(self) -> List[List[MovingState]]:
        """
        Retrieves a list of all looping paths, where each path is composed of a series of MovingState instances.

        This function explores all possible paths from a unique starting state, identifying loops in the process.
        A loop is defined as a series of MovingState objects that eventually return to a previously visited state.

        Returns:
            List[List[MovingState]]: A list containing all looping paths, with each path being a list of MovingState objects.
        """

        # Initialize necessary variables for path exploration and loop detection.
        start_state: MovingState = self.acquire_unique_start(self.token_pool)  # Starting state for path exploration
        search_queue: Queue[MovingState] = Queue(maxsize=1)  # queue to keep track of states yet to explore
        search_queue.put(start_state)
        loops: List[List[MovingState]] = []  # List to store loops found during exploration

        # Variables for managing path tracking, branch depths, and rollback operations within the search algorithm.
        chain: List[MovingState] = []  # Current path being explored
        branch_dict: Dict[MovingState, int] = {}  # Dictionary to track the depth of exploration for each state
        rolling_back: bool = False  # Flag indicating if the exploration is rolling back due to a loop detection
        rollback_to_start: bool = False  # Flag indicating if the exploration is rolling back to the start state
        # Main loop to explore all possible paths and identify loops
        while not rollback_to_start:
            # Pop the current state from the stack for exploration
            cur_state: MovingState = search_queue.get(False)

            # Attempt to find a connected forward transition from the current state
            connected_transition: MovingTransition = self.acquire_connected_forward_transition(
                cur_state, none_check=False
            )

            # Decision making based on the presence of a connected transition and the current exploration status
            match rolling_back, bool(connected_transition):
                case True, False:
                    # This case should theoretically never be reached, indicating a logic error
                    raise ValueError("Should not arrive here!")
                case True, True:

                    # Handling rollback and progression through a loop
                    connected_states = list(connected_transition.to_states.values())
                    cur_depth_index: int = branch_dict.get(cur_state)
                    if cur_depth_index == len(connected_states):
                        if hash(cur_state) == hash(start_state):
                            rollback_to_start = True
                            continue
                        # Loop completion, backtracking to continue exploration
                        search_queue.put(chain.pop())
                    else:
                        branch_dict[cur_state] = cur_depth_index + 1

                        # Progressing to the next state within the loop
                        next_state = connected_states[cur_depth_index]
                        chain.append(cur_state)
                        search_queue.put(next_state)
                        rolling_back = False
                case False, False:
                    # Backtracking to continue exploration from a previous state
                    rolling_back = True
                    search_queue.put(chain.pop())
                    continue
                case False, True:
                    # Progressing to a new state and potentially identifying a loop
                    connected_states = list(connected_transition.to_states.values())

                    cur_depth_index: int = branch_dict.get(cur_state, 0)

                    if cur_depth_index == len(connected_states):
                        # Loop completion, preparing for backtracking
                        rolling_back = True
                        search_queue.put(chain.pop())
                    else:
                        chain.append(cur_state)  # Add current state to the current path
                        branch_dict[cur_state] = cur_depth_index + 1
                        # Checking for and handling loop detection
                        next_state = connected_states[cur_depth_index]
                        state_hash = hash(next_state)
                        if any(state_hash == hash(state) for state in chain):
                            # Loop detected, appending the loop path to the loops list
                            loops.append(chain[chain.index(next_state):])
                            rolling_back = True
                            search_queue.put(chain.pop())
                            continue

                        # Adding the new state to the chain and continuing exploration
                        search_queue.put(next_state)

        return loops  # Returning the list of identified loops

    def is_branchless_chain(self, start_state: MovingState, end_state: MovingState) -> bool:
        """
        Check if the given start state and end state form a branchless chain in the token pool.

        This function ensures the structure validity of the token pool and checks the accessibility of the start state and end state.
        It then performs a breadth-first search to check if there is a path from the start state to the end state in the token pool.
        A branchless chain is defined as a path where each state has only one outgoing transition.

        Parameters:
            start_state (MovingState): The starting state of the chain.
            end_state (MovingState): The end state of the chain.

        Returns:
            bool: True if the start state and end state form a branchless chain, False otherwise.
        """
        self.ensure_structure_validity(self.token_pool)
        self.ensure_accessibility(self.token_pool, start_state, {end_state})

        search_queue = [start_state]
        while search_queue:
            cur_state = search_queue.pop(0)
            connected_transitions: MovingTransition = self.acquire_connected_forward_transition(cur_state)

            match len(connected_transitions.to_states):
                case 1:
                    search_queue.append(list(connected_transitions.to_states.values())[0])
                case _:
                    return False
            if search_queue[-1] == end_state:
                return True

    def acquire_connected_forward_transition(
            self, state: MovingState, none_check: bool = True
    ) -> MovingTransition | None:
        """
        Returns the MovingTransition object that is connected to the given MovingState object in the token pool.

        This function takes in a MovingState object and checks if it is connected to any forward transition in the token pool. It filters the token pool based on the from_states attribute of each transition and returns the first matching MovingTransition object. If none_check is True and no matching transition is found, a ValueError is raised. If none_check is False and no matching transition is found, None is returned. If multiple matching transitions are found, a ValueError is raised.

        Parameters:
            state (MovingState): The MovingState object to search for connected forward transitions.
            none_check (bool, optional): Whether to raise a ValueError if no matching transition is found. Defaults to True.

        Returns:
            MovingTransition | None: The MovingTransition object that is connected to the given MovingState object, or None if none_check is False and no matching transition is found.

        Raises:
            ValueError: If no matching transition is found and none_check is True, or if multiple matching transitions are found.
        """
        response = list(filter(lambda trans: state in set(trans.from_states), self.token_pool))
        match len(response):
            case 0:
                if none_check:
                    raise ValueError(f"the state of {state} is not connected to any forward transition!")
                return None
            case 1:
                return response[0]
            case _:
                err_out = "\n".join(str(x) for x in response)
                raise ValueError(
                    f"A state can *ONLY* connect to ONE transition as its input. Found conflicting transitions:\n {err_out}"
                )

    def acquire_connected_backward_transition(
            self, state: MovingState, none_check: bool = True
    ) -> MovingTransition | List[MovingTransition] | None:
        """
        Returns the MovingTransition object or a list of MovingTransition objects that are connected to the given MovingState object in the token pool.

        This function takes in a MovingState object and checks if it is connected to any backward transition in the token pool. It filters the token pool based on the to_states attribute of each transition and returns the matching MovingTransition object(s). If none_check is True and no matching transition is found, a ValueError is raised. If none_check is False and no matching transition is found, None is returned. If multiple matching transitions are found, a list of the matching MovingTransition objects is returned.

        Parameters:
            state (MovingState): The MovingState object to search for connected backward transitions.
            none_check (bool, optional): Whether to raise a ValueError if no matching transition is found. Defaults to True.

        Returns:
            MovingTransition | List[MovingTransition] | None: The MovingTransition object or a list of MovingTransition objects that are connected to the given MovingState object, or None if none_check is False and no matching transition is found.

        Raises:
            ValueError: If no matching transition is found and none_check is True, or if multiple matching transitions are found.
        """
        response = list(filter(lambda trans: state in trans.to_states.values(), self.token_pool))
        match len(response):
            case 0:
                if none_check:
                    raise ValueError(f"the state of {state} is not connected to any backward transition!")
                return None
            case 1:
                return response[0]
            case _:
                return response

    def _validate_token_pool(self):
        self.ensure_structure_validity(self.token_pool)
        start_state = self.acquire_unique_start(self.token_pool)
        end_states = self.acquire_end_states(self.token_pool)
        self.ensure_accessibility(self.token_pool, start_state, end_states)
        if self.acquire_loops():
            raise ValueError("Loops detected! All State-Transition should be implemented without loops.")

    def _assembly_match_cases(self, match_expression: str | List[str], cases: Dict[KT, str | List[str]]) -> List[str]:
        """
        Assembles a list of strings representing match cases based on the given match expression and cases dictionary.

        Parameters:
            match_expression (str): The match expression to be used.
            cases (Dict[str, str]): A dictionary containing the cases and their corresponding values.

        Returns:
            List[str]: A list of strings representing the match cases.
        """
        match_expression = "".join(match_expression) if isinstance(match_expression, list) else match_expression

        lines: List[str] = [f"match {match_expression}:"]
        for key, value in cases.items():
            case_expr: str = f"'{key}'" if isinstance(key, str) else f"{key}"
            lines.append(self._add_indent(f"case {case_expr}:", count=1))
            lines.extend(self._add_indent(value.split("\n") if isinstance(value, str) else value, count=2))
        lines.append(self._add_indent(f"case undefined:", count=1))
        lines.append(
            self._add_indent(
                f"raise ValueError(f'No matching case found, got {{undefined}}, not in {list(cases.keys())}')", count=2
            )
        )
        return lines

    @staticmethod
    def _add_indent(lines: T_EXPR, indent: str = "    ", count: int = 1) -> T_EXPR:
        """
        Adds an indent to each line in the given list of lines or string.

        Parameters:
            lines (T_EXPR): The list of lines or string to add an indent to.
            indent (str, optional): The string to use for the indent. Defaults to " ".

        Returns:
            T_EXPR: The list of lines with the indent added, or the string with the indent added.
        """
        final_indent = indent * count
        match lines:
            case line_seq if isinstance(line_seq, list) and all((isinstance(line, str) for line in line_seq)):
                return [f"{final_indent}{line}" for line in line_seq]
            case lines_string if isinstance(lines_string, str):
                lines_string: str
                lines_list = lines_string.split("\n")
                return "\n".join(f"{final_indent}{line}" for line in lines_list)
            case _:
                raise TypeError(f"Expected list or string, but got {type(lines)}")

    def acquire_max_branchless_chain(self, start: MovingState) -> Tuple[List[MovingState], List[MovingTransition]]:
        """
        Retrieves the longest branchless chain of states starting from the given initial state.

        Parameters:
        - start: MovingState, the starting state for the search.

        Returns:
        - List[MovingState], the longest branchless chain of states from the start to some terminal state.
        """

        # Initialize the search queue and the longest branchless chain
        search_queue: Queue[MovingState] = Queue(maxsize=1)
        search_queue.put(start)
        max_chain_states: List[MovingState] = []
        max_chain_transitions: List[MovingTransition] = []
        # Perform a breadth-first search
        while not search_queue.empty():
            cur_state = search_queue.get()  # Get the current state

            # Attempt to acquire the next state connected to the current one
            connected_transition: MovingTransition | None = self.acquire_connected_forward_transition(
                cur_state, none_check=False
            )

            max_chain_states.append(cur_state)  # Add the current state to the max chain

            match connected_transition:
                case None:
                    # If no next state, end the search path
                    pass
                case branchless_transition if len(branchless_transition.to_states) == 1:
                    # If the next state is branchless, enqueue it for further search
                    max_chain_transitions.append(branchless_transition)
                    search_queue.put(list(branchless_transition.to_states.values())[0])
                case _:
                    # If the next state has branches, ignore and continue with other paths
                    pass

        return max_chain_states, max_chain_transitions

    @staticmethod
    def _compile_branchless_chain(
            states: List[MovingState],
            transitions: List[MovingTransition],
            controller: Optional[CloseLoopController] = None,
    ) -> Tuple[List[str], Context]:
        """
        Retrieves information from states and transitions to compile a branchless chain.

        Parameters:
            - self: The current instance of the class.
            - states: A list of MovingState objects representing the states in the chain.
            - transitions: A list of MovingTransition objects representing the transitions between states.
            - controller: An optional CloseLoopController object, defaulting to None.

        Returns:
            - Tuple[List[str], Context]: A tuple containing a list of strings representing compiled branchless chain tokens and a context dictionary.

        Note:
            This function compiles a branchless chain by analyzing the states and transitions provided.
        """
        states = list(states)
        transitions = list(transitions)
        context: Context = {}
        state_temp_data = states.pop(0).tokenize(controller)
        ret: List[str] = []
        ret.extend(state_temp_data[0])
        context.update(state_temp_data[1])

        for state, transition in zip(states, transitions):
            state: MovingState
            transition: MovingTransition
            match state.tokenize(controller), transition.tokenize():
                case (state_tokens, state_context), (transition_tokens, transition_context):
                    ret.extend(transition_tokens)
                    context.update(transition_context)
                    ret.extend(state_tokens)
                    context.update(state_context)
        return ret, context

    def _recursive_compile_tokens(self, start: MovingState, controller_name: str, context: Context) -> List[str]:
        """
        Compiles the tokens for a recursive chain of states starting from the given `start` state.

        Args:
            start (MovingState): The starting state of the chain.
            context (Context): The context dictionary to update with the compiled tokens.

        Returns:
            List[str]: A list of strings representing the compiled tokens.

        This function recursively compiles the tokens for a chain of states starting from the given `start` state. It first
        retrieves the maximum branchless chain from the `start` state using the `acquire_max_branchless_chain` method.
        Then, it compiles the tokens for the branchless chain using the `_compile_branchless_chain` method and updates
        the `context` dictionary with the compiled tokens. If the maximum branchless chain has a connected forward
        transition, the function recursively compiles the tokens for the forward states and appends them to the
        `compiled_lines` list. Finally, the function returns the `compiled_lines` list.
        """
        # Initialize an empty list to hold the compiled lines of tokens
        compiled_lines: List[str] = []

        # Retrieve the maximum branchless chain from the starting state
        max_branchless_chain = self.acquire_max_branchless_chain(start=start)

        # Compile the tokens for the acquired branchless chain and update context
        compiled_tokens, compiled_context = self._compile_branchless_chain(
            *max_branchless_chain, controller=self.controller
        )
        context.update(compiled_context)

        line = f"{controller_name}" + "".join(compiled_tokens)

        # Check if the last state in the branchless chain has a connected forward transition
        match max_branchless_chain:
            case ([*_, last_state], _) if connected_forward_transition := self.acquire_connected_forward_transition(
                    last_state, none_check=False
            ):

                branch_transition, branch_context = connected_forward_transition.tokenize()
                context.update(branch_context)
                match_expr = line + "".join(branch_transition)
                match_branch: Dict[KT, List[str]] = {}
                for case, value in connected_forward_transition.to_states.items():
                    match_branch[case] = self._recursive_compile_tokens(
                        start=value, context=context, controller_name=controller_name
                    )
                lines = self._assembly_match_cases(match_expression=match_expr, cases=match_branch)
                return lines
            case _:
                compiled_lines.append(line)
                # If no forward transition is present, return the compiled lines
                return compiled_lines

    @classmethod
    def export_structure(
            cls,
            save_path: str | Path,
            transitions: TokenPool,
            arrow_style: ArrowStyle | Literal["up", "down", "left", "right"] = "down",
    ) -> Self:
        """
        Export the structure to a UML file based on the provided transitions.

        Args:
            save_path (str): The path to save the UML file.
            transitions (Optional[List[MovingTransition]]): The list of transitions to represent in the UML.
            arrow_style (Optional[ArrowStyle]): The style of the arrows to use in the UML. Defaults to "down".
        Returns:
            Self: The current instance.
        """
        undefined_to_state = "UNDEFINED_TO_STATE"
        undefined_from_state = "UNDEFINED_FROM_STATE"
        long_seperator = "\n" + repr("#" * 80) + "\n\n"

        arrow = ArrowStyle.new(arrow_style)

        all_states: Set[MovingState] = set(
            chain(*[transition.from_states + list(transition.to_states.values()) for transition in transitions])
        )
        trunk: List[str] = list(chain(*[cls._generate_state_meta_info(state) for state in all_states]))
        trunk.append(long_seperator)

        for transition in transitions:

            for from_state in list(map(lambda sta: sta.label, transition.from_states)) or [undefined_from_state]:

                match len(transition.to_states):
                    case 0:
                        trunk.append(f"{from_state} {arrow} {undefined_to_state}\n")
                    case 1:
                        to_state = list(transition.to_states.values())[0]
                        trunk.append(f"{from_state} {arrow} {to_state.label}\n")
                    case _:
                        if not callable(transition.breaker):
                            raise ValueError(
                                "The break function must be callable. Since branch must need a valid breaker."
                            )
                        break_node_name = f'{transition.label}_break'
                        trunk.extend(
                            [f"state {break_node_name} <<choice>>\n",
                             f"note right of {break_node_name}: {get_function_annotations(transition.breaker)}\n",
                             f"{from_state} {arrow} {break_node_name}\n", ] +
                            [f"\t{break_node_name} {arrow} {to_state.label}: {case_name}\n"
                             for case_name, to_state in transition.to_states.items()])
        trunk.append(long_seperator)

        cls._compose(trunk, transitions, save_path, arrow)
        return cls

    @classmethod
    def _compose(cls, trunk: List[str], transitions: TokenPool, save_path: str, arrow: ArrowStyle):
        start_heads: List[str] = [f"[*] {arrow} {sta.label}\n" for sta in
                                  (Botix.acquire_start_states(token_pool=transitions))]
        end_heads: List[str] = [f"{sta.label} {arrow} [*]\n" for sta in
                                (Botix.acquire_end_states(token_pool=transitions))]
        start_string = "@startuml\n"
        end_string = "@enduml\n"
        with open(Path(save_path), "w") as f:
            f.writelines([start_string, *trunk, "\n", *start_heads, "\n", *end_heads, "\n", end_string])

    @classmethod
    def _generate_state_meta_info(
            cls,
            state: MovingState,
    ) -> List[str]:

        state_cmds_expr = bold((string := str(state))[string.index("("):])
        before_entering_desc = (
            f"{bold('Before:')}\\n"
            + "\\n".join(f"##{get_function_annotations(fun)}" for fun in state.before_entering)
            + "\\n"
            if state.before_entering
            else ""
        )
        after_entering_desc = (
            f"{bold('After:')}\\n"
            + "\\n".join(f"##{get_function_annotations(fun)}" for fun in state.after_exiting)
            + "\\n"
            if state.after_exiting
            else ""
        )
        if before_entering_desc or after_entering_desc:
            description = f"{state_cmds_expr}\\n====\\n{before_entering_desc}{after_entering_desc}"
        else:
            description = state_cmds_expr
        info_lines: List[str] = [f'state {state.label}: {description}\n']
        return info_lines

    def compile(
            self, return_median: bool = False, function_name: str = "_botix_func"
    ) -> Callable[[], None] | Tuple[List[str], Context]:
        """
        Compiles the bot's code and returns a callable function or a tuple of compiled lines and context.

        Args:
            return_median (bool, optional): Whether to return the compiled lines and context instead of a callable function. Defaults to False.
            function_name (str, optional): The name of the function to be created. Defaults to "_func".

        Returns:
            Callable[[], None] | Tuple[List[str], Context]: The compiled function or a tuple of compiled lines and context.

        Raises:
            None

        Description:
            This function compiles the bot's code and returns a callable function that can be executed. It first checks the requirements of the bot's code using the `_check_met_requirements` method. Then, it creates a function name, function head, and controller name. It initializes an empty context dictionary with the controller name as the key and the bot's controller as the value.

            It retrieves the unique start state from the token pool using the `acquire_unique_start` method.

            Next, it compiles the tokens for the recursive chain of states using the `_recursive_compile_tokens` method. It adds the function head to the beginning of the compiled lines and adds the necessary indentation.

            If `return_median` is True, it returns the compiled lines and context as a tuple. Otherwise, it executes the compiled lines using the `exec` function and retrieves the compiled function from the context dictionary. The compiled function is then returned.
        """

        self._validate_token_pool()
        function_head = f"def {function_name}():"
        controller_name = "con"
        context: Context = {controller_name: self.controller}

        start_state: MovingState = self.acquire_unique_start(self.token_pool)

        function_lines = self._add_indent(
            self._recursive_compile_tokens(start=start_state, context=context, controller_name=controller_name)
        )
        function_lines.insert(0, function_head)

        if return_median:
            return function_lines, context
        exec("\n".join(function_lines), context)
        compiled_obj: Callable[[], None] = context.get(function_name)
        return compiled_obj

    @staticmethod
    def validate_callables(ctx: Context) -> str:
        """
        验证上下文中的所有项是否为可调用对象，并返回一个总结表。

        Args:
            ctx: 包含各种可调用对象的上下文字典
        Returns:
            格式化后的表格字符串，展示每个可调用对象的名称及其调用结果
        """
        # 初始化表格数据，包含表头
        table_data = [["Key", "Function Name", "Return Value"]]

        # 遍历上下文中的每个项
        for key, value in ctx.items():
            # 检查项是否为可调用对象
            if callable(value):  # 检查value是否可调用
                try:
                    # 调用可调用对象，并获取结果
                    result = value()  # 尝试调用该函数
                    # 根据结果是否为None，决定使用的颜色标记
                    if result is None:
                        table_data.append([key, value.__name__, f"{Fore.YELLOW}{result}{Fore.RESET}"])
                        continue
                    table_data.append([key, value.__name__, f"{Fore.GREEN}{result}{Fore.RESET}"])
                except Exception as e:  # 捕获调用过程中可能发生的异常
                    # 如果调用失败，记录异常信息
                    table_data.append([key, value.__name__, f"{Fore.RED}{e}{Fore.RESET}"])

        # 使用SingleTable类生成并返回格式化的表格字符串
        return SingleTable(table_data).table


