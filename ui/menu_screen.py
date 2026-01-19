"""
Menu Screen for Turkish Draughts.

Main menu with game configuration options.
Returns GameSettings when user starts a match.
"""

import flet as ft
from typing import Callable, Optional
import random

from game.types import GameSettings, GameMode, Difficulty, Player
from ui.theme import COLORS, SIZES


def create_menu_screen(
    on_start_game: Callable[[GameSettings], None],
) -> ft.Container:
    """
    Create the main menu screen.
    
    Args:
        on_start_game: Callback with GameSettings when user clicks Start
        
    Returns:
        Flet Container with the menu UI
    """
    # State variables (using Refs for mutability)
    selected_mode = {"value": GameMode.AI}
    selected_difficulty = {"value": Difficulty.MEDIUM}
    selected_time = {"value": None}  # None = untimed
    selected_side = {"value": None}  # None = random
    
    # References to controls that need updating
    difficulty_section_ref = ft.Ref[ft.Container]()
    
    def handle_mode_change(mode: GameMode):
        """Handle game mode selection."""
        selected_mode["value"] = mode
        # Show/hide difficulty section based on mode
        if difficulty_section_ref.current:
            difficulty_section_ref.current.visible = (mode == GameMode.AI)
            difficulty_section_ref.current.update()
    
    def handle_difficulty_change(difficulty: Difficulty):
        """Handle difficulty selection."""
        selected_difficulty["value"] = difficulty
    
    def handle_time_change(time_value: Optional[int]):
        """Handle time control selection."""
        selected_time["value"] = time_value
    
    def handle_side_change(side: Optional[Player]):
        """Handle side selection."""
        selected_side["value"] = side
    
    def handle_start():
        """Handle Start Match button click."""
        # Determine player side
        player_side = selected_side["value"]
        if player_side is None:
            player_side = random.choice([Player.WHITE, Player.BLACK])
        
        # Create settings
        settings = GameSettings(
            mode=selected_mode["value"],
            difficulty=selected_difficulty["value"],
            time_limit=selected_time["value"],
            player_side=player_side,
        )
        on_start_game(settings)
    
    # === UI Components ===
    
    # Title
    title = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "DAMA",
                    size=SIZES["font_3xl"],
                    weight=ft.FontWeight.BOLD,
                    color=COLORS["text_white"],
                ),
                ft.Text(
                    "Turkish Draughts",
                    size=SIZES["font_lg"],
                    color=COLORS["text_gray"],
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SIZES["spacing_xs"],
        ),
        alignment=ft.alignment.center,
        padding=SIZES["spacing_xl"],
    )
    
    def create_mode_button(label: str, mode: GameMode, icon: str) -> ft.Container:
        """Create a mode selection button."""
        is_selected = selected_mode["value"] == mode
        
        def on_click(e):
            handle_mode_change(mode)
            # Update both buttons
            e.page.update()
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        icon,
                        color=COLORS["text_white"] if is_selected else COLORS["text_gray"],
                        size=24,
                    ),
                    ft.Text(
                        label,
                        size=SIZES["font_md"],
                        weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL,
                        color=COLORS["text_white"] if is_selected else COLORS["text_gray"],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=SIZES["spacing_sm"],
            ),
            width=180,
            height=SIZES["button_height"],
            bgcolor=COLORS["primary"] if is_selected else COLORS["surface"],
            border=ft.border.all(
                2,
                COLORS["primary"] if is_selected else COLORS["glass_border"],
            ),
            border_radius=SIZES["radius_md"],
            alignment=ft.alignment.center,
            on_click=on_click,
        )
    
    # Mode selection
    mode_section = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Game Mode",
                    size=SIZES["font_sm"],
                    color=COLORS["text_gray"],
                ),
                ft.Row(
                    [
                        create_mode_button("Play vs AI", GameMode.AI, ft.Icons.SMART_TOY),
                        create_mode_button("Local Match", GameMode.LOCAL, ft.Icons.PEOPLE),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=SIZES["spacing_md"],
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SIZES["spacing_sm"],
        ),
    )
    
    def create_difficulty_card(label: str, difficulty: Difficulty) -> ft.Container:
        """Create a difficulty selection card."""
        is_selected = selected_difficulty["value"] == difficulty
        
        def on_click(e):
            handle_difficulty_change(difficulty)
            e.page.update()
        
        return ft.Container(
            content=ft.Text(
                label,
                size=SIZES["font_sm"],
                weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL,
                color=COLORS["text_white"] if is_selected else COLORS["text_gray"],
            ),
            width=90,
            height=40,
            bgcolor=COLORS["primary"] if is_selected else COLORS["surface"],
            border=ft.border.all(
                1,
                COLORS["primary"] if is_selected else COLORS["glass_border"],
            ),
            border_radius=SIZES["radius_sm"],
            alignment=ft.alignment.center,
            on_click=on_click,
        )
    
    # Difficulty section (only for AI mode)
    difficulty_section = ft.Container(
        ref=difficulty_section_ref,
        content=ft.Column(
            [
                ft.Text(
                    "Difficulty",
                    size=SIZES["font_sm"],
                    color=COLORS["text_gray"],
                ),
                ft.Row(
                    [
                        create_difficulty_card("Easy", Difficulty.EASY),
                        create_difficulty_card("Medium", Difficulty.MEDIUM),
                        create_difficulty_card("Hard", Difficulty.HARD),
                        create_difficulty_card("Master", Difficulty.GRANDMASTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=SIZES["spacing_xs"],
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SIZES["spacing_sm"],
        ),
        visible=True,  # Shown by default since AI is default mode
    )
    
    def create_time_option(label: str, value: Optional[int]) -> ft.Container:
        """Create a time control option."""
        is_selected = selected_time["value"] == value
        
        def on_click(e):
            handle_time_change(value)
            e.page.update()
        
        return ft.Container(
            content=ft.Text(
                label,
                size=SIZES["font_sm"],
                color=COLORS["text_white"] if is_selected else COLORS["text_gray"],
            ),
            width=70,
            height=36,
            bgcolor=COLORS["primary"] if is_selected else COLORS["surface"],
            border=ft.border.all(
                1,
                COLORS["primary"] if is_selected else COLORS["glass_border"],
            ),
            border_radius=SIZES["radius_sm"],
            alignment=ft.alignment.center,
            on_click=on_click,
        )
    
    # Time control section
    time_section = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Time Control",
                    size=SIZES["font_sm"],
                    color=COLORS["text_gray"],
                ),
                ft.Row(
                    [
                        create_time_option("None", None),
                        create_time_option("3 min", 180),
                        create_time_option("5 min", 300),
                        create_time_option("10 min", 600),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=SIZES["spacing_xs"],
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SIZES["spacing_sm"],
        ),
    )
    
    def create_side_option(label: str, value: Optional[Player], icon: str) -> ft.Container:
        """Create a side selection option."""
        is_selected = selected_side["value"] == value
        
        def on_click(e):
            handle_side_change(value)
            e.page.update()
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(
                        icon,
                        color=COLORS["text_white"] if is_selected else COLORS["text_gray"],
                        size=20,
                    ),
                    ft.Text(
                        label,
                        size=SIZES["font_xs"],
                        color=COLORS["text_white"] if is_selected else COLORS["text_gray"],
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
            width=70,
            height=56,
            bgcolor=COLORS["primary"] if is_selected else COLORS["surface"],
            border=ft.border.all(
                1,
                COLORS["primary"] if is_selected else COLORS["glass_border"],
            ),
            border_radius=SIZES["radius_sm"],
            alignment=ft.alignment.center,
            on_click=on_click,
        )
    
    # Side selection section
    side_section = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Play As",
                    size=SIZES["font_sm"],
                    color=COLORS["text_gray"],
                ),
                ft.Row(
                    [
                        create_side_option("White", Player.WHITE, ft.Icons.CIRCLE),
                        create_side_option("Random", None, ft.Icons.SHUFFLE),
                        create_side_option("Black", Player.BLACK, ft.Icons.CIRCLE_OUTLINED),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=SIZES["spacing_sm"],
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SIZES["spacing_sm"],
        ),
    )
    
    # Start button
    start_button = ft.Container(
        content=ft.Text(
            "START MATCH",
            size=SIZES["font_lg"],
            weight=ft.FontWeight.BOLD,
            color=COLORS["text_white"],
        ),
        width=280,
        height=56,
        bgcolor=COLORS["accent_green"],
        border_radius=SIZES["radius_lg"],
        alignment=ft.alignment.center,
        on_click=lambda e: handle_start(),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color="#00B89440",
            offset=ft.Offset(0, 4),
        ),
    )
    
    # Main container
    menu_container = ft.Container(
        content=ft.Column(
            [
                title,
                ft.Container(height=SIZES["spacing_lg"]),
                mode_section,
                ft.Container(height=SIZES["spacing_md"]),
                difficulty_section,
                ft.Container(height=SIZES["spacing_md"]),
                time_section,
                ft.Container(height=SIZES["spacing_md"]),
                side_section,
                ft.Container(height=SIZES["spacing_xl"]),
                start_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=COLORS["bg_dark"],
        padding=SIZES["spacing_xl"],
        expand=True,
    )
    
    return menu_container
