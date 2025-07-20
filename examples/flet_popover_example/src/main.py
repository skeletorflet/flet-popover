import flet as ft
from flet_popover import FletPopover, PopoverDirection, PopoverTransition


def main(page: ft.Page):
    page.title = "FletPopover Examples"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    def on_popover_dismissed(e):
        print("Popover was dismissed!")
        # page.show_snack_bar(ft.SnackBar(content=ft.Text("Popover dismissed!")))

    # Example 1: Basic Popover
    basic_popover = FletPopover(
        content=ft.ElevatedButton(
            text="Basic Popover",
            icon=ft.Icons.INFO,
            on_click=lambda e: basic_popover.open(),
        ),
        body=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "This is a basic popover!", size=16, weight=ft.FontWeight.BOLD
                    ),
                    ft.Text("Click outside to dismiss."),
                    ft.Divider(),
                    ft.ElevatedButton("Action Button", icon=ft.Icons.STAR),
                ],
                tight=True,
            ),
            padding=15,
        ),
        direction=PopoverDirection.BOTTOM,
        width=250,
        height=150,
        on_pop=on_popover_dismissed,
    )

    # Example 2: Styled Popover with different direction
    styled_popover = FletPopover(
        content=ft.Container(
            content=ft.Text("Styled Popover", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.BLUE,
            padding=10,
            border_radius=8,
        ),
        body=ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.PALETTE, size=40, color=ft.Colors.PURPLE),
                    ft.Text(
                        "Custom Styled Popover", size=18, weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(
                        "This popover has custom styling and appears on the right."
                    ),
                    ft.Row(
                        [
                            ft.TextButton("Cancel"),
                            ft.ElevatedButton("OK"),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                tight=True,
            ),
            padding=20,
        ),
        direction=PopoverDirection.RIGHT,
        background_color=ft.Colors.PURPLE_50,
        barrier_color=ft.Colors.BLACK26,
        radius=12,
        arrow_width=20,
        arrow_height=10,
        width=300,
        height=200,
        on_pop=on_popover_dismissed,
    )

    # Example 3: List Menu Popover
    def on_menu_item_click(item):
        def handler(e):
            print(e)

        return handler

    menu_items = [
        ("New File", ft.Icons.ADD, on_menu_item_click("New File")),
        ("Open", ft.Icons.FOLDER_OPEN, on_menu_item_click("Open")),
        ("Save", ft.Icons.SAVE, on_menu_item_click("Save")),
        ("Export", ft.Icons.DOWNLOAD, on_menu_item_click("Export")),
    ]

    menu_popover = FletPopover(
        content=ft.IconButton(
            icon=ft.Icons.MORE_VERT,
            tooltip="Show menu",
            on_click=lambda e: menu_popover.open(),
        ),
        body=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(icon),
                        title=ft.Text(title),
                        on_click=handler,
                        hover_color=ft.Colors.GREY_100,
                        min_height=0,
                    )
                    for title, icon, handler in menu_items
                ],
                tight=True,
                spacing=0,
            ),
            padding=5,
            expand=True
        ),
        direction=PopoverDirection.BOTTOM,
        barrier_dismissible=True,
        on_pop=on_popover_dismissed,
    )

    # Example 4: Form Popover
    name_field = ft.TextField(label="Name", width=200)
    email_field = ft.TextField(label="Email", width=200)

    form_popover = None  # Declare first to use in functions

    def submit_form(e):
        if name_field.value and email_field.value:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(
                        f"Submitted: {name_field.value}, {email_field.value}"
                    )
                )
            )
            name_field.value = ""
            email_field.value = ""
            if form_popover:
                form_popover.close()  # Close the popover after submit
            page.update()

    def cancel_form(e):
        name_field.value = ""
        email_field.value = ""
        if form_popover:
            form_popover.close()  # Close the popover on cancel
        page.update()

    form_popover = FletPopover(
        content=ft.OutlinedButton(
            text="Quick Form",
            icon=ft.Icons.EDIT,
            on_click=lambda e: form_popover.open(),
        ),
        body=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Quick Contact Form", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    name_field,
                    email_field,
                    ft.Row(
                        [
                            ft.TextButton("Cancel", on_click=cancel_form),
                            ft.ElevatedButton("Submit", on_click=submit_form),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                tight=True,
            ),
            padding=20,
        ),
        direction=PopoverDirection.TOP,
        barrier_dismissible=False,  # Must use form buttons to close
        on_pop=on_popover_dismissed,
    )

    # Example 5: Programmatic Control
    programmatic_popover = FletPopover(
        content=ft.Text("Hover me!", size=16),
        body=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Programmatically Controlled", weight=ft.FontWeight.BOLD),
                    ft.Text("This popover can be shown/hidden via code."),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        "Close", on_click=lambda _: programmatic_popover.close()
                    ),
                ],
                tight=True,
                alignment=ft.MainAxisAlignment.END,
            ),
            padding=15,
        ),
        direction=PopoverDirection.LEFT,
        width=250,
        # height=120,
    )

    def show_programmatic(_):
        programmatic_popover.open()

    # Example 6: Content Opcional (Invisible Popover)
    invisible_popover = FletPopover(
        content=None,  # No content - invisible trigger
        body=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Invisible Trigger!", weight=ft.FontWeight.BOLD),
                    ft.Text("This popover has no visible trigger."),
                    ft.Text("It can only be opened programmatically."),
                    ft.ElevatedButton(
                        "Close", on_click=lambda _: invisible_popover.close()
                    ),
                ],
                tight=True,
            ),
            padding=20,
        ),
        direction=PopoverDirection.BOTTOM,
    )

    def show_invisible(_):
        invisible_popover.open()

    # Example 7: External Control
    external_popover = FletPopover(
        content=ft.Container(
            content=ft.Text("I'm controlled externally!", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN,
            padding=10,
            border_radius=8,
        ),
        body=ft.Container(
            content=ft.Column(
                [
                    ft.Text("External Control Demo", weight=ft.FontWeight.BOLD),
                    ft.Text("This popover can be opened/closed from external buttons."),
                    ft.Text("Try the buttons below!"),
                ],
                tight=True,
            ),
            padding=20,
        ),
        direction=PopoverDirection.TOP,
    )

    # Example 6: Different Transitions
    fade_popover = FletPopover(
        content=ft.Chip(
            label=ft.Text("Fade Transition"),
            leading=ft.Icon(ft.Icons.ANIMATION),
        ),
        body=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Fade Transition", weight=ft.FontWeight.BOLD),
                    ft.Text("This popover uses fade transition."),
                    ft.Icon(ft.Icons.START, size=40, color=ft.Colors.BLUE),
                ],
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        ),
        direction=PopoverDirection.TOP,
        transition=PopoverTransition.FADE,
        width=200,
        height=150,
    )

    # Layout the examples
    page.add(
        ft.Text("FletPopover Examples", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("Basic Examples", size=18, weight=ft.FontWeight.W_500),
        ft.Row(
            [
                basic_popover,
                styled_popover,
                menu_popover,
            ],
            wrap=True,
            spacing=20,
        ),
        ft.Divider(),
        ft.Text("Advanced Examples", size=18, weight=ft.FontWeight.W_500),
        ft.Row(
            [
                form_popover,
                ft.Column(
                    [
                        ft.ElevatedButton(
                            "Show Programmatic", on_click=show_programmatic
                        ),
                        programmatic_popover,
                    ],
                    tight=True,
                ),
                fade_popover,
            ],
            wrap=True,
            spacing=20,
        ),
        ft.Divider(),
        ft.Text("New Features", size=18, weight=ft.FontWeight.W_500),
        ft.Row(
            [
                # Invisible popover demo
                ft.Column(
                    [
                        ft.Text("Invisible Popover:", weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("Show Invisible", on_click=show_invisible),
                        ft.Row([invisible_popover], alignment=ft.MainAxisAlignment.END),  # This is invisible but exists
                    ],
                    tight=True,
                ),
                # External control demo
                ft.Column(
                    [
                        ft.Text("External Control:", weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Open", on_click=lambda _: external_popover.open()
                                ),
                                ft.OutlinedButton(
                                    "Close", on_click=lambda _: external_popover.close()
                                ),
                            ]
                        ),
                        external_popover,
                    ],
                    tight=True,
                ),
            ],
            wrap=True,
            spacing=20,
        ),
        ft.Divider(),
        ft.Text("Tips:", size=16, weight=ft.FontWeight.W_500),
        ft.Column(
            [
                ft.Text("• Click on any trigger to show its popover"),
                ft.Text("• Most popovers can be dismissed by clicking outside"),
                ft.Text("• The form popover requires using its buttons to close"),
                ft.Text("• Use open() and close() methods for programmatic control"),
                ft.Text("• Set content=None for invisible triggers"),
                ft.Text("• Try different screen sizes to see responsive behavior"),
                ft.Text("• Try different screen sizes to see responsive behavior"),
            ],
            spacing=5,
        ),
    )


if __name__ == "__main__":
    ft.app(main)
