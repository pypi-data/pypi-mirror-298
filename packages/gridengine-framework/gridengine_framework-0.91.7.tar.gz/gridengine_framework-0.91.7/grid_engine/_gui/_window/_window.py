from . import *

import grid_engine
from grid_engine._utility import generate_images

class GridEngineUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Grid Engine')
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Left panel for viewport
        self.viewport = GEGraphicsView()
        self.scene = QGraphicsScene()
        self.viewport.setScene(self.scene)
        self.main_layout.addWidget(self.viewport, 7)

        # Right panel for controls
        self.control_panel = QWidget()
        self.control_layout = QVBoxLayout(self.control_panel)
        self.main_layout.addWidget(self.control_panel, 3)

        # Text inputs for rows, columns, and resolution
        self.create_text_input('Rows', 1000, self.control_layout, self.update_resolution)
        self.create_text_input('Columns', 1000, self.control_layout, self.update_resolution)
        self.create_text_input('X Resolution', 1000, self.control_layout, self.update_grid_dimensions)
        self.create_text_input('Y Resolution', 1000, self.control_layout, self.update_grid_dimensions)

        # Sliders
        self.sliders = {}
        self.create_slider('Cell Size', 1, 10, 1, self.control_layout)
        self.create_slider('Noise Scale', 100, 1000, 455, self.control_layout)
        self.create_slider('Noise Octaves', 1, 100, 88, self.control_layout)
        self.create_slider('Noise Roughness', 0, 100, 63, self.control_layout)

        # Connect cell size slider to update function
        self.sliders['Cell Size'].valueChanged.connect(self.update_resolution)

        # Buttons
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton('Generate')
        self.generate_button.clicked.connect(self.generate_grid)
        button_layout.addWidget(self.generate_button)

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_grid)
        button_layout.addWidget(self.save_button)

        self.reset_view_button = QPushButton('Reset View')
        self.reset_view_button.clicked.connect(self.reset_view)
        button_layout.addWidget(self.reset_view_button)

        self.control_layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel('Ready')
        self.control_layout.addWidget(self.status_label)

        self.grid = None
        self.cell_size = None
        self.selected_cell_item = None

        # Initial update
        self.update_resolution()

    def create_text_input(self, name, default_value, layout, callback=None):
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel(name))
        text_input = QLineEdit(str(default_value))
        text_input.setValidator(QIntValidator(1, 100000))  # Allow integers from 1 to 100000
        if callback:
            text_input.textChanged.connect(callback)
        input_layout.addWidget(text_input)
        layout.addLayout(input_layout)
        setattr(self, f"{name.lower().replace(' ', '_')}_input", text_input)

    def create_slider(self, name, min_value, max_value, default_value, layout):
        slider_layout = QVBoxLayout()
        slider_layout.addWidget(QLabel(name))
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(default_value)
        slider_layout.addWidget(slider)
        value_label = QLabel(str(default_value))
        slider.valueChanged.connect(lambda value: value_label.setText(str(value)))
        slider_layout.addWidget(value_label)
        layout.addLayout(slider_layout)
        self.sliders[name] = slider

    def update_resolution(self):
        try:
            rows = int(self.rows_input.text())
            columns = int(self.columns_input.text())
            cell_size = self.sliders['Cell Size'].value()

            x_resolution = columns * cell_size
            y_resolution = rows * cell_size

            self.x_resolution_input.setText(str(x_resolution))
            self.y_resolution_input.setText(str(y_resolution))
        except ValueError:
            pass  # Ignore if the input is not a valid integer

    def update_grid_dimensions(self):
        try:
            x_resolution = int(self.x_resolution_input.text())
            y_resolution = int(self.y_resolution_input.text())
            cell_size = self.sliders['Cell Size'].value()

            columns = x_resolution // cell_size
            rows = y_resolution // cell_size

            self.rows_input.setText(str(rows))
            self.columns_input.setText(str(columns))
        except ValueError:
            pass  # Ignore if the input is not a valid integer

    def generate_grid(self):
        self.status_label.setText('Generating grid...')
        try:
            rows = int(self.rows_input.text())
            columns = int(self.columns_input.text())
            self.cell_size = self.sliders['Cell Size'].value()
            noise_scale = self.sliders['Noise Scale'].value()
            noise_octaves = self.sliders['Noise Octaves'].value()
            noise_roughness = self.sliders['Noise Roughness'].value() / 100  # Convert to 0-1 range

            self.status_label.setText(f'Generating grid with {rows} rows, {columns} columns, '
                                      f'cell size {self.cell_size}, noise scale {noise_scale}, '
                                      f'noise octaves {noise_octaves}, noise roughness {noise_roughness}...')

            self.grid = grid_engine.grid.Grid(cell_size=self.cell_size, dimensions=(columns, rows),
                                              noise_scale=noise_scale, noise_octaves=noise_octaves,
                                              noise_roughness=noise_roughness)

            self.status_label.setText('Grid generated successfully. Generating image...')

            cdata = grid_engine.grid.extract_cell_data(self.grid)
            grid_id = self.grid.grid_id[-5:]
            height = self.grid.blueprint.grid_height
            width = self.grid.blueprint.grid_width

            # Use the external generate_images function
            image_path = generate_images((width, height), cdata, self.cell_size, grid_id, display=False)
            image_path.replace('.png', '.tiff')
            self.status_label.setText(f'Image generated successfully. Path: {image_path}')

            # Load and display the image
            self.load_and_display_image(image_path)

            # Hide controls
            self.control_panel.hide()

        except Exception as e:
            self.status_label.setText(f'Error: {str(e)}')
            
    def load_and_display_image(self, image_path):
        try:
            # Load the image from the file
            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                raise Exception("Failed to load the image")

            # Clear the previous scene content
            self.scene.clear()

            # Add the new pixmap to the scene
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(pixmap_item)
            self.scene.setSceneRect(QRectF(pixmap.rect()))

            # Connect mouse click event
            pixmap_item.setAcceptHoverEvents(True)
            pixmap_item.mousePressEvent = self.on_cell_click

            # Fit the view to the new scene content
            self.reset_view()

            self.status_label.setText('Image loaded and displayed successfully.')
        except Exception as e:
            self.status_label.setText(f'Error loading image: {str(e)}')

    def on_cell_click(self, event):
        if not self.grid or not self.cell_size:
            return

        if event.button() == Qt.RightButton:
            pos = event.pos()
            col = int(pos.x() // self.cell_size)
            row = int(pos.y() // self.cell_size)

            if 0 <= col < self.grid.blueprint.grid_width and 0 <= row < self.grid.blueprint.grid_height:
                cell = self.grid[col, row]
                cell_entry = cell.entry
                cell_array = cell.array
                
                cell_data = {}
                
                for dict_ in cell_array:
                    for key, value in dict_.items():
                        cell_data[key] = value
                
                for key, value in cell_entry.items():
                    cell_data[key] = value

                # Remove previous selection
                if self.selected_cell_item:
                    self.scene.removeItem(self.selected_cell_item)

                # Highlight selected cell
                self.selected_cell_item = QGraphicsRectItem(col * self.cell_size, row * self.cell_size, 
                                                            self.cell_size, self.cell_size)
                self.selected_cell_item.setPen(QPen(QColor(255, 0, 0), 0.5))  # Red outline
                self.scene.addItem(self.selected_cell_item)

                # Show cell data
                dialog = CellDataDialog(cell_data, self)
                dialog.exec_()