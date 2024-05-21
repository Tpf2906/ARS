""" main.py used to run the game """
# disabling pylint no-member error for pygame
# pylint: disable=no-member
import os
import pygame
import pygame_gui
from maze import Maze
from config.maze_config import WIDTH, HEIGHT, CELL_SIZE, WHITE, FONT
from config.robot_config import ROBOT_SPEED
from robot import Robot
from evolutionary_algorithm import EvolutionaryAlgorithm
import numpy as np
from fitness import fitness


class MazeGame:
    """
    Handle game initialization and the main game loop.
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Maze Robot Simulation")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.maze = Maze(WIDTH, HEIGHT, CELL_SIZE)
        self.robot = Robot(self.maze, (CELL_SIZE * 1.5, CELL_SIZE * 1.5))
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.setup_gui()
        self.gui_changes = {
            "sensor_noise": [self.robot.sensor_noise],
            "wheel_noise": [self.robot.wheel_noise],
            "kalman_interval": [],
            "Q_t": [self.robot.noise_covariance_measurement_true],
            "Q_F": [self.robot.noise_covariance_measurement_false],
            "R_x": [self.robot.kalman_filter.noise_covariance[0][0]],
            "R_y": [self.robot.kalman_filter.noise_covariance[1][1]],
            "R_t": [self.robot.kalman_filter.noise_covariance[2][2]],
        }
        self.evo_algorithm = EvolutionaryAlgorithm(population_size=8, input_size=15, hidden_size=10, output_size=2, robot=self.robot)
        if os.path.exists('ann_weights.npy'):
            best_weights = np.load('ann_weights.npy')
            self.evo_algorithm.population[0].set_weights(best_weights)

    def setup_gui(self):
        """
        Setup the GUI elements for the game.
        """
        
        # sensor noise caption
        self.sensor_noise_caption = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, HEIGHT - 30), (100, 20)),
            text="Sensor Noise:",
            manager=self.manager
        )
        # sensor noise input
        self.sensor_noise_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((110, HEIGHT - 30), (50, 20)),
            manager=self.manager
        )
        self.sensor_noise_entry.set_text(str(self.robot.sensor_noise))

        ##############################################################

        # wheel noise caption
        self.wheel_noise_caption = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((160, HEIGHT - 30), (100, 20)),
            text="Wheel Noise:",
            manager=self.manager
        )
        # wheel noise input
        self.wheel_noise_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((255, HEIGHT - 30), (50, 20)),
            manager=self.manager
        )
        self.wheel_noise_entry.set_text(str(self.robot.wheel_noise))

        ##############################################################

        # kalman filter call interval caption
        self.kalman_interval_caption = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((290, HEIGHT - 30), (150, 20)),
            text="Kalman Interval:",
            manager=self.manager
        )
        # kalman filter call interval input
        self.kalman_interval_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((420, HEIGHT - 30), (50, 20)),
            manager=self.manager
        )
        self.kalman_interval_entry.set_text(str(self.robot.kalman_call_interval))

        ##############################################################

        # place holder q matrix 1
        self.q_matrix_1 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((460, HEIGHT - 30), (50, 20)),
            text="Q_t:",
            manager=self.manager
        )
        # place holder q matrix 1 input
        self.q_matrix_1_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((495, HEIGHT - 30), (50, 20)),
            manager=self.manager
        )
        self.q_matrix_1_entry.set_text(str(self.robot.noise_covariance_measurement_true))

        ##############################################################

        # place holder q matrix 2
        self.q_matrix_2 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((535, HEIGHT - 30), (50, 20)),
            text="Q_F:",
            manager=self.manager
        )
        # place holder q matrix 2 input
        self.q_matrix_2_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((570, HEIGHT - 30), (50, 20)),
            manager=self.manager
        )
        self.q_matrix_2_entry.set_text(str(self.robot.noise_covariance_measurement_false))

        ##############################################################
        
        # place holder R matrix 1
        self.r_matrix_1 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((610, HEIGHT - 30), (50, 20)),
            text="R_x:",
            manager=self.manager
        )
        # place holder R matrix 1 input
        self.r_matrix_1_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((645, HEIGHT - 30), (50, 20)),
            manager=self.manager
        )
        self.r_matrix_1_entry.set_text(str(self.robot.kalman_filter.noise_covariance[0][0]))

        ##############################################################

        # place holder R matrix 2
        self.r_matrix_2 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((680, HEIGHT - 30), (50, 20)),
            text="R_y:",
            manager=self.manager
        )
        # place holder R matrix 2 input
        self.sensor_r_matrix_2_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((720, HEIGHT - 30), (50, 20)),
            manager=self.manager
        )
        self.sensor_r_matrix_2_entry.set_text(str(self.robot.kalman_filter.noise_covariance[1][1]))

        ##############################################################
        
        # place holder R matrix 3
        self.r_matrix_3 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((760, HEIGHT - 30), (50, 20)),
            text="R_t:",
            manager=self.manager
        )
        # place holder R matrix 3 input
        self.r_matrix_3_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((790, HEIGHT - 30), (50, 20)),
            manager=self.manager
        )
        self.r_matrix_3_entry.set_text(str(self.robot.kalman_filter.noise_covariance[2][2]))
        
        # restore defaults button
        self.restore_defaults_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH - 150, HEIGHT - 30), (150, 20)),
            text='Restore Defaults',
            manager=self.manager,
            object_id="restore_defaults_button"
        )


    def run(self):
        """
        Run the main game loop.
        """
        running = True
        counter = 0
        generations = 8 # number of generations in evolutionary algorithm
        # trains the robot using the evolutionary algorithm for n generations
        for generation in range(generations):
            self.evo_algorithm.evolve()
        
        # save the best individual for experimentation
        best_individual = max(self.evo_algorithm.population, key=lambda ind: fitness(self.robot, ind))
        np.save('ann_weights.npy', best_individual.get_weights())

        while running:
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # pass event to the manager
                self.manager.process_events(event)
                
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    # process text input for each configuration parameter
                    if event.ui_element == self.sensor_noise_entry:
                        try:
                            value = float(event.text)
                            if 0 <= value <= 1:
                                self.robot.sensor_noise = value
                                print(f"Sensor noise: {value}")
                        except ValueError:
                            self.sensor_noise_entry.set_text(str(self.robot.sensor_noise))# reset to default value

                    elif event.ui_element == self.wheel_noise_entry:
                        try:
                            value = float(event.text)
                            if 0 <= value <= 1:
                                self.robot.wheel_noise = value
                                print(f"Wheel noise: {value}")
                        except ValueError:
                            self.wheel_noise_entry.set_text(str(self.robot.wheel_noise))  # reset to default value

                    elif event.ui_element == self.kalman_interval_entry:
                        try:
                            value = int(event.text)
                            if 1 <= value:
                                self.robot.kalman_call_interval = value
                                print(f"Kalman interval: {value}")
                        except ValueError:
                            self.kalman_interval_entry.set_text(str(self.robot.kalman_call_interval))  # reset to default value

                    elif event.ui_element == self.q_matrix_1_entry:
                        try:
                            value = float(event.text)
                            self.robot.noise_covariance_measurement_true = value
                            print(f"Q_t: {value}")
                        except ValueError:
                            self.q_matrix_1_entry.set_text(str(self.robot.noise_covariance_measurement_true))

                    elif event.ui_element == self.q_matrix_2_entry:
                        try:
                            value = float(event.text)
                            self.robot.noise_covariance_measurement_false = value
                            print(f"Q_F: {value}")
                        except ValueError:
                            self.q_matrix_2_entry.set_text(str(self.robot.noise_covariance_measurement_false))

                    elif event.ui_element == self.r_matrix_1_entry:
                        try:
                            value = float(event.text)
                            self.robot.kalman_filter.noise_covariance[0][0] = value
                            print(f"R_x: {value}")
                        except ValueError:
                            self.r_matrix_1_entry.set_text(str(self.robot.kalman_filter.noise_covariance[0][0]))

                    elif event.ui_element == self.sensor_r_matrix_2_entry:
                        try:
                            value = float(event.text)
                            self.robot.kalman_filter.noise_covariance[1][1] = value
                            print(f"R_y: {value}")
                        except ValueError:
                            self.sensor_r_matrix_2_entry.set_text(str(self.robot.kalman_filter.noise_covariance[1][1]))

                    elif event.ui_element == self.r_matrix_3_entry:
                        try:
                            value = float(event.text)
                            self.robot.kalman_filter.noise_covariance[2][2] = value
                            print(f"R_t: {value}")
                        except ValueError:
                            self.r_matrix_3_entry.set_text(str(self.robot.kalman_filter.noise_covariance[2][2]))

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.restore_defaults_button:
                        self.robot.restore_defaults()  # restore default values
                        self.sensor_noise_entry.set_text(str(self.robot.sensor_noise))
                        self.wheel_noise_entry.set_text(str(self.robot.wheel_noise))
                        self.kalman_interval_entry.set_text(str(self.robot.kalman_call_interval))

            self.manager.update(time_delta)
            
            sensors = self.robot.sensors
            position = (self.robot.x, self.robot.y)
            angle = self.robot.angle
            inputs = np.concatenate((sensors, [position[0], position[1], angle]))

            vl, vr = best_individual.forward(inputs)

            # move the robot
            if vr != 0 or vl != 0:

                # move the robot with the diff drive model
                self.robot.move_with_diff_drive(vl, vr)

                if counter % self.robot.kalman_call_interval == 0:
                    # run the kalman filter
                    self.robot.run_kalman_filter(vl, vr)

                    # store the sensor noise for plotting
                    self.gui_changes["sensor_noise"].append(self.robot.sensor_noise)

                    # store the wheel noise for plotting
                    self.gui_changes["wheel_noise"].append(self.robot.wheel_noise)

                    #TODO fix so that kalman interval can be changed during runtime, ploting is breaking
                    # store the kalman interval for plotting
                    #self.gui_changes["kalman_interval"].append(self.robot.kalman_call_interval)

                    # store the Q_t for plotting
                    self.gui_changes["Q_t"].append(self.robot.noise_covariance_measurement_true)

                    # store the Q_F for plotting
                    self.gui_changes["Q_F"].append(self.robot.noise_covariance_measurement_false)

                    # store the R_x for plotting
                    self.gui_changes["R_x"].append(self.robot.kalman_filter.noise_covariance[0][0])

                    # store the R_y for plotting
                    self.gui_changes["R_y"].append(self.robot.kalman_filter.noise_covariance[1][1])

                    # store the R_t for plotting
                    self.gui_changes["R_t"].append(self.robot.kalman_filter.noise_covariance[2][2])

            # create the speed text
            speed_text = FONT.render(f'wheel power: {vl} | {vr}', True, WHITE)

            # reset the wheel power, to avoid continuous movement
            vr, vl = 0, 0

            # draw the maze, robot and speed cltext
            self.screen.fill(WHITE)
            self.maze.draw(self.screen)
            self.robot.draw_landmark_raycast(self.screen)
            self.robot.draw_path(self.screen)
            self.robot.update_sensors()
            self.robot.draw(self.screen)
            self.manager.draw_ui(self.screen)
            self.screen.blit(speed_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)
            counter += 1

        pygame.quit()
        
    def handle_controls(self, keys):
        """
        Handle the controls for the robot.
        """
        # set the wheel power to 0
        vr, vl = 0, 0

        # if w is pressed, move the robot forward by 1
        if keys[pygame.K_w]:
            vr, vl = 1, 1

        # if s is pressed, move the robot backward by 1
        elif keys[pygame.K_s]:
            vr, vl = -1, -1

        # if a is pressed, turn the robot left
        if keys[pygame.K_a]:
            vr += 0.5
            vl += -0.5

        # if d is pressed, turn the robot right
        if keys[pygame.K_d]:
            vr += -0.5
            vl += 0.5

        # invert the controls, pygame treats the y axis as inverted
        vl, vr = vr * ROBOT_SPEED , vl * ROBOT_SPEED

        return vr, vl
    
def plot_extra_data(self, passed_indices, passed_plot):

    # plot the sensor noise
    passed_plot.plot(passed_indices, self.gui_changes["sensor_noise"][-len(-passed_indices):], label="sensor noise")

    # plot the wheel noise
    passed_plot.plot(passed_indices, self.gui_changes["wheel_noise"][-len(passed_indices):], label="wheel noise")

    #TODO: add after fixing the kalman interval, unchangable during runtime
    # plot the kalman interval

    # plot the Q_t
    passed_plot.plot(passed_indices, self.gui_changes["Q_t"][-len(passed_indices):], label="Q_t")

    # plot the Q_F
    passed_plot.plot(passed_indices, self.gui_changes["Q_F"][-len(passed_indices):], label="Q_F")

    # plot the R_x
    passed_plot.plot(passed_indices, self.gui_changes["R_x"][-len(passed_indices):], label="R_x")

    # plot the R_y
    passed_plot.plot(passed_indices, self.gui_changes["R_y"][-len(passed_indices):], label="R_y")

    # plot the R_t
    passed_plot.plot(passed_indices, self.gui_changes["R_t"][-len(passed_indices):], label="R_t")
    

    # add legend
    passed_plot.legend()

    return passed_indices, passed_plot



if __name__ == "__main__":
    game = MazeGame()
    game.run()
    indices, plot = game.robot.plot_error()
    indices, plot = plot_extra_data(game, indices, plot)
    plot.show()
