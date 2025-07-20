from enum import Enum
from typing import Any, Optional, List, Union
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.types import (
    ColorValue,
    OptionalControlEventCallable,
    BorderRadius,
    Duration,
    ColorEnums
)


class PopoverDirection(Enum):
    """
    Popover direction enum.
    """

    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"


class PopoverTransition(Enum):
    """
    Popover transition enum.
    """

    SCALE = "scale"
    FADE = "fade"


class FletPopover(ConstrainedControl):
    """
    A popover is a transient view that appears above other content onscreen when you tap a control or in an area.

    Typically, a popover includes an arrow pointing to the location from which it emerged.
    Popovers can be nonmodal or modal. A nonmodal popover is dismissed by tapping another part
    of the screen or a button on the popover. A modal popover is dismissed by tapping a Cancel
    or other button on the popover.

    This control wraps the Flutter popover package to provide popover functionality in Flet.
    """

    def __init__(
        self,
        #
        # ConstrainedControl
        #
        ref=None,
        key=None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[dict] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[dict] = None,
        scale: Optional[dict] = None,
        offset: Optional[dict] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[dict] = None,
        animate_size: Optional[dict] = None,
        animate_position: Optional[dict] = None,
        animate_rotation: Optional[dict] = None,
        animate_scale: Optional[dict] = None,
        animate_offset: Optional[dict] = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        badge: Optional[dict] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
        #
        # FletPopover specific
        #
        body: Control = None,  # body is now required
        content: Optional[Control] = None,  # content is optional
        direction: Optional[PopoverDirection] = PopoverDirection.BOTTOM,
        transition: Optional[PopoverTransition] = PopoverTransition.SCALE,
        background_color: Optional[ColorValue] = None,
        barrier_color: Optional[ColorValue] = None,
        transition_duration: Optional[Duration] = None,
        radius: OptionalNumber = None,
        border_radius: Optional[BorderRadius] = None,
        arrow_width: OptionalNumber = None,
        arrow_height: OptionalNumber = None,
        arrow_dx_offset: OptionalNumber = None,
        arrow_dy_offset: OptionalNumber = None,
        content_dx_offset: OptionalNumber = None,
        content_dy_offset: OptionalNumber = None,
        barrier_dismissible: Optional[bool] = None,
        modal: Optional[bool] = None,
        on_pop: OptionalControlEventCallable = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
            rtl=rtl,
        )

        # Initialize private attributes
        self.__content = None
        self.__body = None
        self.__direction = None
        self.__transition = None
        self.__background_color = None
        self.__barrier_color = None

        # Validate required parameters
        if body is None:
            raise ValueError("body parameter is required for FletPopover")
        
        # Set properties through setters to ensure proper attribute setting
        self.content = content
        self.body = body
        self.direction = direction
        self.transition = transition
        self.background_color = background_color
        self.barrier_color = barrier_color
        self.transition_duration = transition_duration
        self.radius = radius
        self.border_radius = border_radius
        self.arrow_width = arrow_width
        self.arrow_height = arrow_height
        self.arrow_dx_offset = arrow_dx_offset
        self.arrow_dy_offset = arrow_dy_offset
        self.content_dx_offset = content_dx_offset
        self.content_dy_offset = content_dy_offset
        self.barrier_dismissible = barrier_dismissible
        self.modal = modal
        self.on_pop = on_pop

    def _get_control_name(self):
        return "flet_popover"

    def _get_children(self):
        children = []
        # body is required, so it should always be present
        if self.__body is not None:
            self.__body._set_attr_internal("n", "body")
            children.append(self.__body)
        # content is optional
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # content - the trigger control that when clicked shows the popover
    @property
    def content(self) -> Optional[Control]:
        """
        The control that triggers the popover when clicked.
        """
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # body - the content inside the popover (required)
    @property
    def body(self) -> Control:
        """
        The content to display inside the popover. This is required.
        """
        return self.__body

    @body.setter
    def body(self, value: Control):
        if value is None:
            raise ValueError("body cannot be None - it is required for FletPopover")
        self.__body = value

    # direction
    @property
    def direction(self) -> Optional[PopoverDirection]:
        """
        The direction where the popover should appear relative to the trigger control.
        """
        return self.__direction

    @direction.setter
    def direction(self, value: Optional[PopoverDirection]):
        self.__direction = value
        self._set_attr("direction", value.value if value else None)

    # transition
    @property
    def transition(self) -> Optional[PopoverTransition]:
        """
        The transition animation to use when showing/hiding the popover.
        """
        return self.__transition

    @transition.setter
    def transition(self, value: Optional[PopoverTransition]):
        self.__transition = value
        self._set_attr("transition", value.value if value else None)

    # background_color
    @property
    def background_color(self) -> Optional[ColorValue]:
        """
        The background color of the popover.
        """
        return self.__background_color

    @background_color.setter
    def background_color(self, value: Optional[ColorValue]):
        self.__background_color = value
        self._set_enum_attr("backgroundColor", value, ColorEnums)

    # barrier_color
    @property
    def barrier_color(self) -> Optional[ColorValue]:
        """
        The color of the barrier (overlay) behind the popover.
        """
        return self.__barrier_color

    @barrier_color.setter
    def barrier_color(self, value: Optional[ColorValue]):
        self.__barrier_color = value
        self._set_enum_attr("barrierColor", value, ColorEnums)

    # transition_duration
    @property
    def transition_duration(self) -> Optional[Duration]:
        """
        The duration of the transition animation.
        """
        return self._get_attr("transitionDuration")

    @transition_duration.setter
    def transition_duration(self, value: Optional[Duration]):
        self._set_attr("transitionDuration", value)

    # radius
    @property
    def radius(self) -> OptionalNumber:
        """
        The border radius of the popover.
        """
        return self._get_attr("radius", data_type="float")

    @radius.setter
    def radius(self, value: OptionalNumber):
        self._set_attr("radius", value)

    # border_radius
    @property
    def border_radius(self) -> Optional[BorderRadius]:
        """
        The border radius of the popover (more detailed than radius).
        """
        return self._get_attr("borderRadius")

    @border_radius.setter
    def border_radius(self, value: Optional[BorderRadius]):
        self._set_attr("borderRadius", value)


    @property
    def arrow_width(self) -> OptionalNumber:
        """
        The width of the popover arrow.
        """
        return self._get_attr("arrowWidth", data_type="float")

    @arrow_width.setter
    def arrow_width(self, value: OptionalNumber):
        self._set_attr("arrowWidth", value)

    # arrow_height
    @property
    def arrow_height(self) -> OptionalNumber:
        """
        The height of the popover arrow.
        """
        return self._get_attr("arrowHeight", data_type="float")

    @arrow_height.setter
    def arrow_height(self, value: OptionalNumber):
        self._set_attr("arrowHeight", value)

    # arrow_dx_offset
    @property
    def arrow_dx_offset(self) -> OptionalNumber:
        """
        The horizontal offset of the popover arrow.
        """
        return self._get_attr("arrowDxOffset", data_type="float")

    @arrow_dx_offset.setter
    def arrow_dx_offset(self, value: OptionalNumber):
        self._set_attr("arrowDxOffset", value)

    # arrow_dy_offset
    @property
    def arrow_dy_offset(self) -> OptionalNumber:
        """
        The vertical offset of the popover arrow.
        """
        return self._get_attr("arrowDyOffset", data_type="float")

    @arrow_dy_offset.setter
    def arrow_dy_offset(self, value: OptionalNumber):
        self._set_attr("arrowDyOffset", value)

    # content_dx_offset
    @property
    def content_dx_offset(self) -> OptionalNumber:
        """
        The horizontal offset of the popover content.
        """
        return self._get_attr("contentDxOffset", data_type="float")

    @content_dx_offset.setter
    def content_dx_offset(self, value: OptionalNumber):
        self._set_attr("contentDxOffset", value)

    # content_dy_offset
    @property
    def content_dy_offset(self) -> OptionalNumber:
        """
        The vertical offset of the popover content.
        """
        return self._get_attr("contentDyOffset", data_type="float")

    @content_dy_offset.setter
    def content_dy_offset(self, value: OptionalNumber):
        self._set_attr("contentDyOffset", value)

    # barrier_dismissible
    @property
    def barrier_dismissible(self) -> Optional[bool]:
        """
        Whether the popover can be dismissed by tapping outside of it.
        """
        return self._get_attr("barrierDismissible", data_type="bool")

    @barrier_dismissible.setter
    def barrier_dismissible(self, value: Optional[bool]):
        self._set_attr("barrierDismissible", value)

    # modal
    @property
    def modal(self) -> Optional[bool]:
        """
        Whether the popover should be modal (blocking interaction with other controls).
        """
        return self._get_attr("modal", data_type="bool")

    @modal.setter
    def modal(self, value: Optional[bool]):
        self._set_attr("modal", value)

    # on_pop
    @property
    def on_pop(self) -> OptionalControlEventCallable:
        """
        Event handler called when the popover is dismissed.
        """
        return self._get_event_handler("on_pop")

    @on_pop.setter
    def on_pop(self, handler: OptionalControlEventCallable):
        self._add_event_handler("on_pop", handler)

    # Methods
    def show_popover(self):
        """
        Show the popover programmatically.
        """
        self.invoke_method("show_popover", wait_for_result=False)

    def hide_popover(self):
        """
        Hide the popover programmatically.
        """
        self.invoke_method("hide_popover", wait_for_result=False)

    def open(self):
        """
        Open the popover programmatically. Alias for show_popover().
        """
        self.show_popover()

    def close(self):
        """
        Close the popover programmatically. Alias for hide_popover().
        """
        self.hide_popover()
