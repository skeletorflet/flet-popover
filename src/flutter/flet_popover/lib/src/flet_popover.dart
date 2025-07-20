import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:popover/popover.dart';

/// Configuration class for optimal popover positioning
class _PopoverConfig {
  final PopoverDirection direction;
  final double? width;
  final double? height;
  final BoxConstraints constraints;

  _PopoverConfig({
    required this.direction,
    this.width,
    this.height,
    required this.constraints,
  });
}

class FletPopoverControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const FletPopoverControl({
    super.key,
    required this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.parentAdaptive,
    required this.backend,
  });

  @override
  State<FletPopoverControl> createState() => _FletPopoverControlState();
}

class _FletPopoverControlState extends State<FletPopoverControl> {
  @override
  void initState() {
    super.initState();
    widget.backend.subscribeMethods(widget.control.id, _onMethodCall);
  }

  @override
  void dispose() {
    widget.backend.unsubscribeMethods(widget.control.id);
    super.dispose();
  }

  Future<String?> _onMethodCall(
      String methodName, Map<String, String> args) async {
    switch (methodName) {
      case "show_popover":
      case "open":
        _showPopover();
        return null;
      case "hide_popover":
      case "close":
        _hidePopover();
        return null;
      default:
        return null;
    }
  }

  void _hidePopover() {
    if (Navigator.canPop(context)) {
      Navigator.of(context).pop();
    }
  }

  void _showPopover() {
    // Get the body control
    var bodyControls = widget.children.where((c) => c.name == "body" && c.isVisible);
    if (bodyControls.isEmpty) {
      debugPrint("FletPopover: No body control found");
      return;
    }

    // Parse original direction preference
    PopoverDirection preferredDirection = _parseDirection(widget.control.attrString("direction", "bottom"));

    // Parse transition
    PopoverTransition transition = _parseTransition(widget.control.attrString("transition", "scale"));

    // Parse colors
    Color? backgroundColor = widget.control.attrColor("backgroundColor", context);
    Color? barrierColor = widget.control.attrColor("barrierColor", context);

    // Parse dimensions and offsets
    double? width = widget.control.attrDouble("width");
    double? height = widget.control.attrDouble("height");
    double radius = widget.control.attrDouble("radius", 8.0)!;
    double arrowWidth = widget.control.attrDouble("arrowWidth", 24.0)!;
    double arrowHeight = widget.control.attrDouble("arrowHeight", 12.0)!;
    double arrowDxOffset = widget.control.attrDouble("arrowDxOffset", 0.0)!;
    double arrowDyOffset = widget.control.attrDouble("arrowDyOffset", 0.0)!;
    double contentDxOffset = widget.control.attrDouble("contentDxOffset", 0.0)!;
    double contentDyOffset = widget.control.attrDouble("contentDyOffset", 0.0)!;

    // Parse behavior
    bool barrierDismissible = widget.control.attrBool("barrierDismissible", true)!;

    // Parse transition duration
    int transitionDurationMs = widget.control.attrInt("transitionDuration", 200)!;
    Duration transitionDuration = Duration(milliseconds: transitionDurationMs);

    // Parse shadow
    List<BoxShadow> shadow = _parseShadow();

    // Create the body widget
    bool? adaptive = widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    Widget bodyWidget = createControl(
      widget.control,
      bodyControls.first.id,
      disabled,
      parentAdaptive: adaptive
    );

    // Get screen dimensions and trigger position
    final screenSize = MediaQuery.of(context).size;
    final renderBox = context.findRenderObject() as RenderBox?;
    
    if (renderBox == null) {
      debugPrint("FletPopover: Could not find render box");
      return;
    }

    final triggerPosition = renderBox.localToGlobal(Offset.zero);
    final triggerSize = renderBox.size;

    // Calculate optimal direction and constraints based on available space
    final optimalConfig = _calculateOptimalPopoverConfig(
      screenSize: screenSize,
      triggerPosition: triggerPosition,
      triggerSize: triggerSize,
      preferredDirection: preferredDirection,
      popoverWidth: width,
      popoverHeight: height,
      arrowHeight: arrowHeight,
    );

    showPopover(
      context: context,
      bodyBuilder: (context) => bodyWidget,
      direction: optimalConfig.direction,
      transition: transition,
      backgroundColor: backgroundColor ?? const Color(0xFFFFFFFF),
      barrierColor: barrierColor ?? const Color(0x80000000),
      transitionDuration: transitionDuration,
      radius: radius,
      shadow: shadow,
      arrowWidth: arrowWidth,
      arrowHeight: arrowHeight,
      arrowDxOffset: arrowDxOffset,
      arrowDyOffset: arrowDyOffset,
      contentDxOffset: contentDxOffset,
      contentDyOffset: contentDyOffset,
      barrierDismissible: barrierDismissible,
      width: optimalConfig.width,
      height: optimalConfig.height,
      constraints: optimalConfig.constraints,
      onPop: () {
        // Trigger the on_pop event
        widget.backend.triggerControlEvent(widget.control.id, "on_pop", "");
      },
    );
  }

  PopoverDirection _parseDirection(String? direction) {
    switch (direction?.toLowerCase()) {
      case "top":
        return PopoverDirection.top;
      case "left":
        return PopoverDirection.left;
      case "right":
        return PopoverDirection.right;
      case "bottom":
      default:
        return PopoverDirection.bottom;
    }
  }

  PopoverTransition _parseTransition(String? transition) {
    switch (transition?.toLowerCase()) {
      case "fade":
        return PopoverTransition.other;
      case "scale":
      default:
        return PopoverTransition.scale;
    }
  }

  List<BoxShadow> _parseShadow() {
    // Default shadow
    List<BoxShadow> defaultShadow = [
      const BoxShadow(
        color: Color(0x1F000000),
        blurRadius: 5,
      )
    ];

    return defaultShadow;
  }

  /// Calculate optimal popover configuration to ensure it stays within screen bounds
  _PopoverConfig _calculateOptimalPopoverConfig({
    required Size screenSize,
    required Offset triggerPosition,
    required Size triggerSize,
    required PopoverDirection preferredDirection,
    double? popoverWidth,
    double? popoverHeight,
    required double arrowHeight,
  }) {
    // Define margins to keep popover away from screen edges
    const double margin = 16.0;
    
    // Calculate available space in each direction
    final double spaceAbove = triggerPosition.dy - margin;
    final double spaceBelow = screenSize.height - (triggerPosition.dy + triggerSize.height) - margin;
    final double spaceLeft = triggerPosition.dx - margin;
    final double spaceRight = screenSize.width - (triggerPosition.dx + triggerSize.width) - margin;
    
    // Estimate popover dimensions if not provided
    final double estimatedWidth = popoverWidth ?? (screenSize.width * 0.6);
    final double estimatedHeight = popoverHeight ?? (screenSize.height * 0.4);
    
    // Add arrow height to required space
    final double requiredHeightWithArrow = estimatedHeight + arrowHeight;
    final double requiredWidthWithArrow = estimatedWidth + arrowHeight; // For left/right directions
    
    // Determine optimal direction based on available space
    PopoverDirection optimalDirection = preferredDirection;
    
    switch (preferredDirection) {
      case PopoverDirection.bottom:
        if (spaceBelow < requiredHeightWithArrow) {
          // Not enough space below, try other directions
          if (spaceAbove >= requiredHeightWithArrow) {
            optimalDirection = PopoverDirection.top;
          } else if (spaceRight >= requiredWidthWithArrow) {
            optimalDirection = PopoverDirection.right;
          } else if (spaceLeft >= requiredWidthWithArrow) {
            optimalDirection = PopoverDirection.left;
          }
          // If no direction has enough space, keep original but constrain size
        }
        break;
        
      case PopoverDirection.top:
        if (spaceAbove < requiredHeightWithArrow) {
          if (spaceBelow >= requiredHeightWithArrow) {
            optimalDirection = PopoverDirection.bottom;
          } else if (spaceRight >= requiredWidthWithArrow) {
            optimalDirection = PopoverDirection.right;
          } else if (spaceLeft >= requiredWidthWithArrow) {
            optimalDirection = PopoverDirection.left;
          }
        }
        break;
        
      case PopoverDirection.right:
        if (spaceRight < requiredWidthWithArrow) {
          if (spaceLeft >= requiredWidthWithArrow) {
            optimalDirection = PopoverDirection.left;
          } else if (spaceBelow >= requiredHeightWithArrow) {
            optimalDirection = PopoverDirection.bottom;
          } else if (spaceAbove >= requiredHeightWithArrow) {
            optimalDirection = PopoverDirection.top;
          }
        }
        break;
        
      case PopoverDirection.left:
        if (spaceLeft < requiredWidthWithArrow) {
          if (spaceRight >= requiredWidthWithArrow) {
            optimalDirection = PopoverDirection.right;
          } else if (spaceBelow >= requiredHeightWithArrow) {
            optimalDirection = PopoverDirection.bottom;
          } else if (spaceAbove >= requiredHeightWithArrow) {
            optimalDirection = PopoverDirection.top;
          }
        }
        break;
    }
    
    // Calculate constrained dimensions based on chosen direction
    double? constrainedWidth = popoverWidth;
    double? constrainedHeight = popoverHeight;
    BoxConstraints constraints;
    
    switch (optimalDirection) {
      case PopoverDirection.top:
      case PopoverDirection.bottom:
        // Constrain height based on available vertical space
        final double availableHeight = (optimalDirection == PopoverDirection.bottom ? spaceBelow : spaceAbove) - arrowHeight;
        constrainedHeight = popoverHeight != null 
            ? (popoverHeight > availableHeight ? availableHeight : popoverHeight)
            : (estimatedHeight > availableHeight ? availableHeight : estimatedHeight);
        
        // Constrain width to screen width with margins
        final double maxScreenWidth = screenSize.width - (2 * margin);
        constrainedWidth = popoverWidth != null
            ? (popoverWidth > maxScreenWidth ? maxScreenWidth : popoverWidth)
            : (estimatedWidth > maxScreenWidth ? maxScreenWidth : estimatedWidth);
            
        constraints = BoxConstraints(
          maxWidth: maxScreenWidth,
          maxHeight: availableHeight,
          minWidth: 100,
          minHeight: 50,
        );
        break;
        
      case PopoverDirection.left:
      case PopoverDirection.right:
        // Constrain width based on available horizontal space
        final double availableWidth = (optimalDirection == PopoverDirection.right ? spaceRight : spaceLeft) - arrowHeight;
        constrainedWidth = popoverWidth != null
            ? (popoverWidth > availableWidth ? availableWidth : popoverWidth)
            : (estimatedWidth > availableWidth ? availableWidth : estimatedWidth);
        
        // Constrain height to screen height with margins
        final double maxScreenHeight = screenSize.height - (2 * margin);
        constrainedHeight = popoverHeight != null
            ? (popoverHeight > maxScreenHeight ? maxScreenHeight : popoverHeight)
            : (estimatedHeight > maxScreenHeight ? maxScreenHeight : estimatedHeight);
            
        constraints = BoxConstraints(
          maxWidth: availableWidth,
          maxHeight: maxScreenHeight,
          minWidth: 100,
          minHeight: 50,
        );
        break;
    }
    
    return _PopoverConfig(
      direction: optimalDirection,
      width: constrainedWidth,
      height: constrainedHeight,
      constraints: constraints,
    );
  }

  @override
  Widget build(BuildContext context) {
    // Get the content (trigger) control
    var contentControls = widget.children.where((c) => c.name == "content" && c.isVisible);

    if (contentControls.isEmpty) {
      // If no content control is provided, return an invisible widget that takes no space
      return IgnorePointer(
        child: Container(
          width: 0,
          height: 0,
        ),
      );
    }

    // Create the content widget with tap handler
    bool? adaptive = widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    Widget contentWidget = createControl(
      widget.control,
      contentControls.first.id,
      disabled,
      parentAdaptive: adaptive
    );

    // Wrap with LayoutBuilder to get accurate viewport information
    return LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        // Wrap the content widget with GestureDetector to handle taps
        return GestureDetector(
          onTap: disabled ? null : _showPopover,
          child: contentWidget,
        );
      },
    );
  }
}
