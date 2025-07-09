import flet as ft
from datetime import datetime, timedelta
import random

class Vehicle:
    def __init__(self, id, name, vehicle_type, current_km, last_maintenance_date, image_path,
                 chofer, modelo_camion, modelo_motor, tipo_mantencion, tipo_aceite, costo_mantencion, observacion, fecha_ingreso="Sin registro"):
        self.id = id
        self.name = name
        self.vehicle_type = vehicle_type
        self.current_km = current_km
        self.last_maintenance_date = last_maintenance_date
        self.image_path = image_path
        self.chofer = chofer
        self.modelo_camion = modelo_camion
        self.modelo_motor = modelo_motor
        self.tipo_mantencion = tipo_mantencion
        self.tipo_aceite = tipo_aceite
        self.costo_mantencion = costo_mantencion
        self.observacion = observacion
        self.fecha_ingreso = fecha_ingreso

    def needs_km_maintenance(self, km_limit=5000):
        return self.current_km >= km_limit

    def needs_date_maintenance(self, days_limit=30):
        days_diff = (datetime.now() - self.last_maintenance_date).days
        return days_diff >= days_limit

    def get_days_since_maintenance(self):
        return (datetime.now() - self.last_maintenance_date).days


class FleetMaintenanceApp:
    def __init__(self):
        self.vehicles = self.create_sample_vehicles()
        self.selected_vehicle = None
        self.page = None

    def create_sample_vehicles(self):
        return [
            Vehicle(1, "Camión Mercedes 001", "Camión", 4800, datetime.now() - timedelta(days=15), "images/camion1.jpg",
                    "Carlos Muñoz", "Actros 1845", "OM471", "Preventiva", "15W-40", 450000, "Sin observaciones."),
            Vehicle(2, "Bus Volvo 002", "Bus", 5200, datetime.now() - timedelta(days=35), "images/bus1.jpg",
                    "Juan Pérez", "Volvo B11R", "D11K460", "Correctiva", "10W-30", 600000, "Reemplazo de filtros."),
            Vehicle(3, "Camión Scania 003", "Camión", 3500, datetime.now() - timedelta(days=8), "images/camion2.jpg",
                    "Andrea Soto", "R450", "DC13", "Preventiva", "15W-40", 420000, "Mantenimiento programado."),
            Vehicle(4, "Bus Mercedes 004", "Bus", 5800, datetime.now() - timedelta(days=45), "images/bus2.jpg",
                    "Pedro Díaz", "O500RS", "OM457", "Correctiva", "10W-40", 550000, "Revisión por ruido en motor.")
        ]

    def main(self, page: ft.Page):
        self.page = page
        page.title = "FlotaSegura - Control Inteligente de Mantención de Flotas"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = ft.Colors.GREY_900
        page.window_width = 1200
        page.window_height = 800
        self.show_welcome_screen()

    def show_welcome_screen(self):
        def go_to_dashboard(e):
            self.build_dashboard()

        welcome_view = ft.Column([
            ft.Image(src="images/logoFlota.jpeg", width=650),
            ft.Text("Sistema inteligente de control de mantenciones de flotas", size=25, color=ft.Colors.GREY_50),
            ft.ElevatedButton(text="INICIAR FlotaSegura",
                              icon=ft.Icons.LOCAL_SHIPPING,
                              on_click=go_to_dashboard,
                              style=ft.ButtonStyle(
                                  shape=ft.RoundedRectangleBorder(radius=5),
                                  padding=5,
                                  bgcolor=ft.Colors.CYAN_700,
                                  color=ft.Colors.GREY_50
                              ),
                              icon_color=ft.Colors.WHITE,
                              width=200,
                              height=50)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        self.page.controls.clear()
        self.page.add(ft.Container(content=welcome_view, expand=True, alignment=ft.alignment.center))
        self.page.update()

    def build_dashboard(self):
        self.vehicle_list_container = ft.Container(content=ft.Column(), width=400, padding=10, bgcolor=ft.Colors.BLUE_100,
                                                   border_radius=5)
        self.detail_container = ft.Container(content=ft.Column(), expand=True, padding=20, bgcolor=ft.Colors.BLUE_50,
                                            border_radius=5, margin=ft.margin.only(left=10))

        title = ft.Text("\U0001F6E0 Panel de Mantención de Vehículos", size=30, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_200)
        btn_salir = ft.TextButton(text="Salir", icon=ft.Icons.EXIT_TO_APP,
                                 style=ft.ButtonStyle(bgcolor=ft.Colors.RED_900, color=ft.Colors.WHITE,
                                                     shape=ft.RoundedRectangleBorder(radius=5)),
                                 on_click=lambda e: self.show_welcome_screen(), width=80)

        btn_agregar = ft.ElevatedButton(
            text="Agregar Nuevo Vehículo",
            icon=ft.Icons.ADD,
            on_click=self.show_add_vehicle_form,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=5),
                padding=10
            )
        )

        btn_calculo = ft.ElevatedButton(
            text="Ver Cálculos / Costos",
            icon=ft.Icons.BAR_CHART,
            on_click=self.show_cost_calculation_page,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=5),
                padding=10
            )
        )

        self.build_vehicle_list()
        self.build_detail_view()

        main_row = ft.Row([self.vehicle_list_container, self.detail_container], expand=True)

        self.page.controls.clear()
        self.page.add(ft.Container(content=ft.Column([
            ft.Row([title, btn_salir], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([btn_agregar, ft.Container(width=20), btn_calculo], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
            main_row]), padding=20))

        self.page.update()

    def build_vehicle_list(self):
        vehicle_cards = []
        for vehicle in self.vehicles:
            alert_color, alert_icon, alert_text = ft.Colors.GREEN, ft.Icons.CHECK_CIRCLE, "OK"
            if vehicle.needs_km_maintenance() or vehicle.needs_date_maintenance():
                alert_color, alert_icon, alert_text = ft.Colors.RED, ft.Icons.WARNING, "ALERTA"
            elif vehicle.current_km > 5000 or vehicle.get_days_since_maintenance() > 30:
                alert_color, alert_icon, alert_text = ft.Colors.ORANGE, ft.Icons.INFO, "PRECAUCIÓN"

            img = ft.Image(src=vehicle.image_path, width=180, height=150, fit=ft.ImageFit.COVER,
                           border_radius=ft.border_radius.all(8))

            card = ft.Container(
                content=ft.Column([
                    img,
                    ft.Container(height=5),
                    ft.Row([
                        ft.Icon(ft.Icons.LOCAL_SHIPPING if vehicle.vehicle_type == "Camión" else ft.Icons.DIRECTIONS_BUS,
                                color=ft.Colors.BLUE_800),
                        ft.Text(vehicle.name, weight=ft.FontWeight.BOLD, expand=True),
                        ft.Container(content=ft.Row([ft.Icon(alert_icon, color=alert_color, size=16),
                                                    ft.Text(alert_text, color=alert_color, size=12,
                                                            weight=ft.FontWeight.BOLD)]), bgcolor=ft.Colors.WHITE, padding=5,
                                     border_radius=5)
                    ]),
                    ft.DataTable(
                        border=ft.border.all(2, ft.Colors.GREY_50),
                        columns=[
                            ft.DataColumn(label=ft.Text("Parámetro", weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(label=ft.Text("Registro", weight=ft.FontWeight.BOLD)),
                        ],
                        rows=[
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Kilometraje")),
                                ft.DataCell(ft.Text(f"{vehicle.current_km:,} km")),
                            ]),
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Últ. mantención")),
                                ft.DataCell(ft.Text(vehicle.last_maintenance_date.strftime('%d/%m/%Y'))),
                            ]),
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Días transcurridos")),
                                ft.DataCell(ft.Text(f"{vehicle.get_days_since_maintenance()} días")),
                            ])
                        ]),
                ]),
                padding=10,
                bgcolor=ft.Colors.BLUE_200,
                border_radius=5,
                on_click=lambda e, v=vehicle: self.select_vehicle(v)
            )
            vehicle_cards.append(card)

        self.vehicle_list_container.content = ft.Column([
            ft.Text("Lista de Vehículos", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
            ft.Divider(),
            ft.Column(vehicle_cards, scroll=ft.ScrollMode.AUTO, height=750)
        ])
        self.page.update()

    def select_vehicle(self, vehicle):
        self.selected_vehicle = vehicle
        self.build_detail_view()
        self.page.update()

    def build_detail_view(self):
        if not self.selected_vehicle:
            self.detail_container.content = ft.Column([
                ft.Container(content=ft.Column([
                    ft.Icon(ft.Icons.DIRECTIONS_CAR, size=100, color=ft.Colors.GREY_300),
                    ft.Text("Selecciona un vehículo para ver los detalles", size=16, color=ft.Colors.GREY_800,
                            text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center, expand=True)
            ])
            return

        v = self.selected_vehicle
        self.detail_container.content = ft.Column([
            ft.Text(f"Detalles: {v.name}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800,
                    text_align=ft.TextAlign.CENTER),
            ft.Divider(),
            ft.Container(content=ft.Image(src=v.image_path, width=200, height=80, fit=ft.ImageFit.CONTAIN),
                         alignment=ft.alignment.center),
            ft.DataTable(
                border=ft.border.all(2, ft.Colors.BLUE_800),
                columns=[
                    ft.DataColumn(label=ft.Text("Parámetro", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(label=ft.Text("Registro", weight=ft.FontWeight.BOLD)),
                ],
                rows=[
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Tipo", size=12)), ft.DataCell(ft.Text(v.vehicle_type))]),
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Chofer", size=12)), ft.DataCell(ft.Text(v.chofer))]),
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Modelo Camión", size=12)), ft.DataCell(ft.Text(v.modelo_camion))]),
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Modelo Motor", size=12)), ft.DataCell(ft.Text(v.modelo_motor))]),
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Tipo Mantención", size=12)), ft.DataCell(ft.Text(v.tipo_mantencion))]),
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Tipo Aceite", size=12)), ft.DataCell(ft.Text(v.tipo_aceite))]),
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Costo Mantención", size=12)),
                                     ft.DataCell(ft.Text(f"${v.costo_mantencion:,}"))]),
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Observación", size=12)), ft.DataCell(ft.Text(v.observacion))]),
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Kilometraje", size=12)),
                                     ft.DataCell(ft.Text(f"{v.current_km:,} km"))]),
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Última mantención", size=12)),
                                     ft.DataCell(ft.Text(v.last_maintenance_date.strftime('%d/%m/%Y')))]),
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Días desde mantención", size=12)),
                                     ft.DataCell(ft.Text(f"{v.get_days_since_maintenance()} días"))]),
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Fecha ingreso", size=12)), ft.DataCell(ft.Text(v.fecha_ingreso))]),
                ]
            )
        ])

        self.page.update()

    def show_cost_calculation_page(self, e):
      btn_volver = ft.ElevatedButton(
        text="Volver a Panel",
        icon=ft.Icons.LOCAL_SHIPPING,
        on_click=lambda e: self.build_dashboard(),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=5))
      )
 
      if not self.selected_vehicle:
        self.page.controls.clear()
        self.page.add(
            ft.Text("No hay vehículo seleccionado para mostrar cálculos.", size=30, color=ft.Colors.BLUE_200),
            ft.Container(height=20),
            btn_volver
        )
        self.page.update()
        return

      v = self.selected_vehicle
      costo_por_km = round(v.costo_mantencion / v.current_km, 2) if v.current_km > 0 else 0
      dias_mantencion = v.get_days_since_maintenance()
      tiempo_estimado = v.current_km / 100
      tasa_cambio = 100
      uso_estimado = 100 * tiempo_estimado + 5 * tiempo_estimado ** 2
      costo_estimado = 40 * v.current_km + 40000

      imagen = ft.Image(
        src=v.image_path,
        width=300,
        height=300,
        fit=ft.ImageFit.CONTAIN,
        border_radius=8
      )

      tabla_datos = ft.DataTable(
        border=ft.border.all(2, ft.Colors.BLUE_800),
        columns=[
            ft.DataColumn(label=ft.Text("Cálculo", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(label=ft.Text("Resultado", weight=ft.FontWeight.BOLD)),
        ],
        rows=[
            ft.DataRow(cells=[ft.DataCell(ft.Text("Kilometraje actual")), ft.DataCell(ft.Text(f"{v.current_km:,} km"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Costo total mantención")), ft.DataCell(ft.Text(f"${v.costo_mantencion:,}"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Costo por kilómetro")), ft.DataCell(ft.Text(f"${costo_por_km}"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Días desde mantención")), ft.DataCell(ft.Text(f"{dias_mantencion} días"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Función lineal k(t)=100t")), ft.DataCell(ft.Text(f"t ≈ {tiempo_estimado:.1f} días"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Derivada k'(t)")), ft.DataCell(ft.Text(f"{tasa_cambio} km/día"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Crecimiento g(t)=100t+5t²")), ft.DataCell(ft.Text(f"{uso_estimado:.1f} km"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Costo estimado C(k)=40k+40000")), ft.DataCell(ft.Text(f"${costo_estimado:,}"))]),
        ]
      )
 
      contenido = ft.Row(
        controls=[
            ft.Container(content=tabla_datos, expand=True, padding=10),
            ft.Container(content=imagen, alignment=ft.alignment.center)
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10
      )

      card = ft.Container(
        content=ft.Column([
            ft.Text(f"🚛 {v.name}", size=25, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_200),
            ft.Divider(),
            contenido
        ]),
        padding=15,
        bgcolor=ft.Colors.BLUE_50,
        border_radius=10
      )
 
      self.page.controls.clear()
      self.page.add(
        ft.Container(
            content=ft.Column([
                ft.Row(
                    controls=[
                        ft.Text("Cálculo de Costos y Análisis Matemático", size=25, weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_200, expand=True),
                        btn_volver
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(color=ft.Colors.WHITE),
                ft.Column([card], scroll=ft.ScrollMode.AUTO, height=850),
            ]),
            padding=20
        )
      )
      self.page.update()

    def show_add_vehicle_form(self, e):
        tipo_field = ft.Dropdown(label="Tipo", options=[
            ft.dropdown.Option("Camión"),
            ft.dropdown.Option("Bus")
        ], color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.WHITE))
        chofer_field = ft.TextField(label="Nombre del chofer", color=ft.Colors.WHITE,
                                   label_style=ft.TextStyle(color=ft.Colors.WHITE))
        modelo_camion_field = ft.TextField(label="Modelo de Vehiculo", color=ft.Colors.WHITE,
                                          label_style=ft.TextStyle(color=ft.Colors.WHITE))
        modelo_motor_field = ft.TextField(label="Modelo del motor", color=ft.Colors.WHITE,
                                         label_style=ft.TextStyle(color=ft.Colors.WHITE))
        tipo_mantencion_field = ft.TextField(label="Tipo de mantención", color=ft.Colors.WHITE,
                                            label_style=ft.TextStyle(color=ft.Colors.WHITE))
        tipo_aceite_field = ft.TextField(label="Tipo de aceite", color=ft.Colors.WHITE,
                                        label_style=ft.TextStyle(color=ft.Colors.WHITE))
        costo_field = ft.TextField(label="Costo de mantención", keyboard_type=ft.KeyboardType.NUMBER,
                                  color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.WHITE))
        observacion_field = ft.TextField(label="Observaciones", color=ft.Colors.WHITE,
                                        label_style=ft.TextStyle(color=ft.Colors.WHITE))
        km_field = ft.TextField(label="Kilometraje actual", keyboard_type=ft.KeyboardType.NUMBER,
                               color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.WHITE))
        fecha_ingreso_field = ft.TextField(label="Fecha de ingreso (dd/mm/aaaa)", color=ft.Colors.WHITE,
                                          label_style=ft.TextStyle(color=ft.Colors.WHITE))
        imagen_field = ft.TextField(label="Imagen", value="Aquí se agrega la imagen", disabled=True, color=ft.Colors.WHITE,
                                   label_style=ft.TextStyle(color=ft.Colors.WHITE),
                                   )
        boton_imagen = ft.ElevatedButton(
            text="Agregar Imagen",
            icon=ft.Icons.IMAGE,
            on_click=lambda e: None,  # no hace nada aún
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=5),
                padding=10,
            )
        )

        def guardar_vehiculo(e):
            try:
                fecha_ingreso_val = datetime.strptime(fecha_ingreso_field.value, "%d/%m/%Y").strftime("%d/%m/%Y")
            except:
                fecha_ingreso_val = "Sin registro"

            if tipo_field.value == "Camión":
                image_path = "images/camion.jpg"
            elif tipo_field.value == "Bus":
                image_path = "images/bus.png"
            else:
                image_path = "images/logoFlota.jpeg"

            nuevo = Vehicle(
                id=len(self.vehicles) + 1,
                name=f"{tipo_field.value} Genérico {len(self.vehicles) + 1}",
                vehicle_type=tipo_field.value,
                chofer=chofer_field.value,
                modelo_camion=modelo_camion_field.value,
                modelo_motor=modelo_motor_field.value,
                tipo_mantencion=tipo_mantencion_field.value,
                tipo_aceite=tipo_aceite_field.value,
                costo_mantencion=int(costo_field.value) if costo_field.value.isdigit() else 0,
                observacion=observacion_field.value,
                current_km=int(km_field.value) if km_field.value.isdigit() else 0,
                last_maintenance_date=datetime.now(),
                fecha_ingreso=fecha_ingreso_val,
                image_path=image_path,
            )
            self.vehicles.append(nuevo)
            self.selected_vehicle = nuevo
            self.build_dashboard()

        def cancelar(e):
            self.build_dashboard()

        form_column = ft.Column([
            ft.Text("\U0001F69A Agregar Nuevo Vehículo", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200),
            ft.Text(""),
            ft.Text(""),
            tipo_field,
            chofer_field,
            modelo_camion_field,
            modelo_motor_field,
            tipo_mantencion_field,
            tipo_aceite_field,
            costo_field,
            observacion_field,
            km_field,
            fecha_ingreso_field,
            imagen_field,
            boton_imagen,
            ft.Text(""),
            ft.Row([
                ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar_vehiculo, style=ft.ButtonStyle(
                    bgcolor=ft.Colors.GREEN_800,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=5),
                    padding=10,
                )),

                ft.ElevatedButton("Cancelar", icon=ft.Icons.CANCEL, on_click=cancelar, style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=5),
                    padding=10,
                ))
            ], alignment=ft.MainAxisAlignment.END)
        ], scroll=ft.ScrollMode.AUTO)
        self.page.bgcolor = ft.Colors.GREY_800
        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=form_column,
                padding=20,
                expand=True,
                alignment=ft.alignment.top_center
            )
        )
        self.page.update()


def main(page: ft.Page):
    app = FleetMaintenanceApp()
    app.main(page)


if __name__ == "__main__":
    ft.app(target=main)
