#!/usr/bin/env python3

import locale
import math
import pygame
import sys
from datetime import datetime


class Clock:
    """
    A class to represent a clock.
    """

    def __init__(self):
        """
        Initializes the clock.
        """
        pygame.init()
        self.WINDOW_SIZE = 400
        self.window = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("Clock")
        self.clock = pygame.time.Clock()
        self.is_stopwatch = False
        self.is_paused = False  # Track pause state
        self.start_time = None
        self.pause_time = None  # Track pause time
        self.paused_elapsed_time = None  # Track elapsed time when paused
        self.font = pygame.font.Font(None, int(self.WINDOW_SIZE * 0.06))
        self.init_constants()

    def init_constants(self):
        """
        Initializes constants for clock dimensions and colors.
        """
        self.CLOCK_RADIUS = int(self.WINDOW_SIZE * 0.375)
        self.CENTER = (self.WINDOW_SIZE // 2, (0.9 * self.WINDOW_SIZE) // 2)
        self.HOUR_MARK_LENGTH = int(self.CLOCK_RADIUS * 0.1)
        self.MINUTE_MARK_LENGTH = int(self.HOUR_MARK_LENGTH * 0.75)
        self.HOUR_MARK_WIDTH = int(self.WINDOW_SIZE * 0.01)
        self.MINUTE_MARK_WIDTH = int(self.HOUR_MARK_WIDTH * 0.5)
        self.HOUR_HAND_LENGTH = int(self.CLOCK_RADIUS * 0.466)
        self.MINUTE_HAND_LENGTH = int(self.CLOCK_RADIUS * 0.625)
        self.SECOND_HAND_LENGTH = int(self.CLOCK_RADIUS * 0.688)

        self.BLACK = (32, 32, 32)
        self.WHITE = (255, 255, 255)
        self.RED = (255 - 32, 0, 0)

    def draw_clock(self):
        """
        Draws the clock face and markings.
        """
        # Draw clock border
        pygame.draw.circle(
            self.window,
            self.BLACK,
            self.CENTER,
            self.CLOCK_RADIUS + int(self.WINDOW_SIZE * 0.0125),
            int(self.WINDOW_SIZE * 0.0125),
        )

        # Draw clock markings and numbers
        for i in range(60):
            angle = math.radians(i * 6)
            if i % 5 == 0:
                length = self.HOUR_MARK_LENGTH
                width = self.HOUR_MARK_WIDTH
                number = str(i // 5 if i != 0 else 12)
                number_surface = self.font.render(number, True, self.BLACK)
                number_rect = number_surface.get_rect(
                    center=(
                        int(
                            self.CENTER[0]
                            + (self.CLOCK_RADIUS - int(self.CLOCK_RADIUS * 0.1875))
                            * math.sin(angle)
                        ),
                        int(
                            self.CENTER[1]
                            - (self.CLOCK_RADIUS - int(self.CLOCK_RADIUS * 0.1875))
                            * math.cos(angle)
                        ),
                    )
                )
                self.window.blit(number_surface, number_rect)
            else:
                length = self.MINUTE_MARK_LENGTH
                width = self.MINUTE_MARK_WIDTH
            start = (
                self.CENTER[0] + (self.CLOCK_RADIUS - length) * math.sin(angle),
                self.CENTER[1] - (self.CLOCK_RADIUS - length) * math.cos(angle),
            )
            end = (
                self.CENTER[0] + self.CLOCK_RADIUS * math.sin(angle),
                self.CENTER[1] - self.CLOCK_RADIUS * math.cos(angle),
            )
            pygame.draw.line(self.window, self.BLACK, start, end, width)

    def draw_hands(self, hour, minute, second):
        """
        Draws the clock hands.
        """
        # Draw hour hand
        hour_angle = math.radians((hour * 30) + (minute / 2))
        hour_end = (
            self.CENTER[0] + self.HOUR_HAND_LENGTH * math.sin(hour_angle),
            self.CENTER[1] - self.HOUR_HAND_LENGTH * math.cos(hour_angle),
        )
        pygame.draw.line(
            self.window,
            self.BLACK,
            self.CENTER,
            hour_end,
            int(self.WINDOW_SIZE * 0.0175),
        )

        # Draw minute hand
        minute_angle = math.radians((minute * 6) + (second / 10))
        minute_end = (
            self.CENTER[0] + self.MINUTE_HAND_LENGTH * math.sin(minute_angle),
            self.CENTER[1] - self.MINUTE_HAND_LENGTH * math.cos(minute_angle),
        )
        pygame.draw.line(
            self.window,
            self.BLACK,
            self.CENTER,
            minute_end,
            int(self.WINDOW_SIZE * 0.0125),
        )

        # Draw second hand
        second_angle = math.radians(second * 6)
        second_end = (
            self.CENTER[0] + self.SECOND_HAND_LENGTH * math.sin(second_angle),
            self.CENTER[1] - self.SECOND_HAND_LENGTH * math.cos(second_angle),
        )
        pygame.draw.line(
            self.window,
            self.RED,
            self.CENTER,
            second_end,
            int(self.WINDOW_SIZE * 0.00875),
        )
        pygame.draw.circle(
            self.window,
            self.RED,
            (int(second_end[0]), int(second_end[1])),
            int(self.WINDOW_SIZE * 0.01),
        )

    def draw_date(self):
        """
        Draws the current date on the clock face.
        """
        current_time = datetime.now()
        locale.setlocale(locale.LC_TIME, "")
        formatted_date = current_time.strftime("%A, %x")
        date_surface = self.font.render(formatted_date, True, self.BLACK)
        date_rect = date_surface.get_rect(
            bottomleft=(int(self.WINDOW_SIZE * 0.025), int(self.WINDOW_SIZE * 0.975))
        )
        self.window.blit(date_surface, date_rect)

    def draw_buttons(self):
        """
        Draws the stopwatch, reset, and pause/resume buttons.
        """
        # Draw stopwatch button
        stopwatch_button_rect = pygame.Rect(
            int(self.WINDOW_SIZE * 0.875),
            int(self.WINDOW_SIZE * 0.875),
            int(self.WINDOW_SIZE * 0.1),
            int(self.WINDOW_SIZE * 0.1),
        )
        stopwatch_radius = int(self.WINDOW_SIZE * 0.01)
        stopwatch_button_color = self.RED if self.is_stopwatch else self.BLACK
        pygame.draw.rect(
            self.window,
            stopwatch_button_color,
            stopwatch_button_rect,
            border_radius=stopwatch_radius,
        )

        # Draw button text
        stopwatch_text = "SW" if self.is_stopwatch else "CL"
        stopwatch_surface = self.font.render(stopwatch_text, True, self.WHITE)
        stopwatch_rect = stopwatch_surface.get_rect(
            center=(int(self.WINDOW_SIZE * 0.925), int(self.WINDOW_SIZE * 0.925))
        )
        self.window.blit(stopwatch_surface, stopwatch_rect)

        # Draw pause/resume button
        if self.is_stopwatch:
            pause_resume_button_rect = pygame.Rect(
                int(self.WINDOW_SIZE * 0.625),
                int(self.WINDOW_SIZE * 0.875),
                int(self.WINDOW_SIZE * 0.1),
                int(self.WINDOW_SIZE * 0.1),
            )
            pause_resume_radius = int(self.WINDOW_SIZE * 0.01)
            pause_resume_button_color = self.RED if self.is_paused else self.BLACK
            pause_resume_text = "| |" if not self.is_paused else ">"
            pause_resume_surface = self.font.render(pause_resume_text, True, self.WHITE)
            pause_resume_rect = pause_resume_surface.get_rect(
                center=(int(self.WINDOW_SIZE * 0.675), int(self.WINDOW_SIZE * 0.925))
            )
            pygame.draw.rect(
                self.window,
                pause_resume_button_color,
                pause_resume_button_rect,
                border_radius=pause_resume_radius,
            )
            self.window.blit(pause_resume_surface, pause_resume_rect)

            reset_text = "R"
            reset_surface = self.font.render(reset_text, True, self.WHITE)
            reset_rect = reset_surface.get_rect(
                center=(int(self.WINDOW_SIZE * 0.8), int(self.WINDOW_SIZE * 0.925))
            )
            reset_button_rect = pygame.Rect(
                int(self.WINDOW_SIZE * 0.75),
                int(self.WINDOW_SIZE * 0.875),
                int(self.WINDOW_SIZE * 0.1),
                int(self.WINDOW_SIZE * 0.1),
            )
            reset_radius = int(self.WINDOW_SIZE * 0.01)
            pygame.draw.rect(
                self.window, self.BLACK, reset_button_rect, border_radius=reset_radius
            )
            self.window.blit(reset_surface, reset_rect)

    def run(self):
        """
        Runs the clock application.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        # Check if clicked on stopwatch button
                        if (
                            self.WINDOW_SIZE * 0.875 <= x <= self.WINDOW_SIZE * 0.975
                            and self.WINDOW_SIZE * 0.875
                            <= y
                            <= self.WINDOW_SIZE * 0.975
                        ):
                            self.is_stopwatch = not self.is_stopwatch
                            if self.is_stopwatch and self.start_time is None:
                                self.start_time = datetime.now()
                        # Check if clicked on reset button
                        elif (
                            self.WINDOW_SIZE * 0.75 <= x <= self.WINDOW_SIZE * 0.85
                            and self.WINDOW_SIZE * 0.875
                            <= y
                            <= self.WINDOW_SIZE * 0.975
                        ):
                            self.pause_time = datetime.now()
                            self.start_time = self.pause_time
                        # Check if clicked on pause/resume button
                        elif (
                            self.is_stopwatch
                            and self.WINDOW_SIZE * 0.625
                            <= x
                            <= self.WINDOW_SIZE * 0.725
                            and self.WINDOW_SIZE * 0.875
                            <= y
                            <= self.WINDOW_SIZE * 0.975
                        ):
                            self.is_paused = not self.is_paused
                            if self.is_paused:
                                self.pause_time = datetime.now()
                            else:
                                if self.paused_elapsed_time:
                                    self.start_time += datetime.now() - self.pause_time
                                    self.paused_elapsed_time = None

            self.window.fill(self.WHITE)
            self.draw_clock()

            if not self.is_stopwatch:
                current_time = datetime.now()
                hour = current_time.hour % 12
                minute = current_time.minute
                second = current_time.second
                self.draw_hands(hour, minute, second)
                self.draw_date()
            else:
                if not self.is_paused:
                    elapsed_time = datetime.now() - self.start_time
                else:
                    elapsed_time = self.pause_time - self.start_time
                    self.paused_elapsed_time = elapsed_time

                self.draw_hands(
                    elapsed_time.seconds // 3600 % 12,
                    elapsed_time.seconds // 60 % 60,
                    elapsed_time.seconds % 60,
                )
                elapsed_time_str = str(elapsed_time).split(".")[0]
                elapsed_surface = self.font.render(elapsed_time_str, True, self.BLACK)
                elapsed_rect = elapsed_surface.get_rect(
                    bottomleft=(
                        int(self.WINDOW_SIZE * 0.025),
                        int(self.WINDOW_SIZE * 0.975),
                    )
                )
                self.window.blit(elapsed_surface, elapsed_rect)

            self.draw_buttons()

            pygame.display.update()
            self.clock.tick(10)


def main():
    """
    Main function to run the clock application.
    """
    Clock().run()


if __name__ == "__main__":
    main()
