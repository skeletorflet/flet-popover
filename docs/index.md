# Introduction

FletPopover for Flet.

## Examples

```
import flet as ft

from flet_popover import FletPopover


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(

                ft.Container(height=150, width=300, alignment = ft.alignment.center, bgcolor=ft.Colors.PURPLE_200, content=FletPopover(
                    tooltip="My new FletPopover Control tooltip",
                    value = "My new FletPopover Flet Control", 
                ),),

    )


ft.app(main)
```

## Classes

[FletPopover](FletPopover.md)


