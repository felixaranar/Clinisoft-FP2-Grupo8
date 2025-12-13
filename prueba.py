from datetime import datetime, date, time

# Clase Persona
class Persona:
    def __init__(self, dni, nombre, apellido, telefono):
        self.__dni = dni
        self.__nombre = nombre
        self.__apellido = apellido
        self.__telefono = telefono

    @property
    def dni(self):
        return self.__dni

    @property
    def nombre_completo(self):
        return f"{self.__nombre} {self.__apellido}"

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        if nuevo_telefono and len(nuevo_telefono.strip()) >= 9:
            self.__telefono = nuevo_telefono.strip()
        else:
            raise ValueError("Error: el teléfono debe tener al menos 9 dígitos")

# Clase Paciente hereda de Persona
class Paciente(Persona):
    def __init__(self, dni, nombre, apellido, telefono, fecha_nacimiento):
        super().__init__(dni, nombre, apellido, telefono)
        self.__fecha_nacimiento = fecha_nacimiento

    def __calcular_edad(self):
        hoy = date.today()
        edad = hoy.year - self.__fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.__fecha_nacimiento.month, self.__fecha_nacimiento.day):
            edad -= 1
        return edad

    def obtener_info(self):
        return f"DNI: {self.dni} | {self.nombre_completo} | Edad: {self.__calcular_edad()}"

# Clase Medico hereda de Persona
class Medico(Persona):
    def __init__(self, dni, nombre, apellido, telefono, especialidad):
        super().__init__(dni, nombre, apellido, telefono)
        self.__especialidad = especialidad
        self.__citas = []

    def agregar_cita(self, cita):
        self.__citas.append(cita)

    @property
    def especialidad(self):
        return self.__especialidad

    @especialidad.setter
    def especialidad(self, nueva_especialidad):
        if nueva_especialidad and nueva_especialidad.strip():
            self.__especialidad = nueva_especialidad.strip()
        else:
            raise ValueError("Error: La especialidad no puede estar vacía")

    @property
    def total_citas(self):
        return len(self.__citas)

# Clase Cita
class Cita:
    def __init__(self, codigo, paciente, medico, fecha, hora):
        self.__codigo = codigo
        self.__paciente = paciente
        self.__medico = medico
        self.__fecha = fecha
        self.__hora = hora

    def mostrar(self):
        return f"{self.__codigo} | {self.__paciente.nombre_completo} | Dr. {self.__medico.nombre_completo} - {self.__medico.especialidad} | {self.__fecha} {self.__hora.strftime('%H:%M')}"

# Clase Clinica
class Clinica:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__pacientes = []
        self.__medicos = []
        self.__citas = []

    def registrar_paciente(self, paciente):
        if any(p.dni == paciente.dni for p in self.__pacientes):
            return False
        self.__pacientes.append(paciente)
        return True

    def buscar_paciente_dni(self, dni):
        for p in self.__pacientes:
            if p.dni == dni:
                return p
        return None

    def buscar_paciente_nombre(self, nombre):
        return [p for p in self.__pacientes if nombre.lower() in p.nombre_completo.lower()]

    def mostrar_pacientes(self):
        if not self.__pacientes:
            print("No hay pacientes registrados.")
            return

        for p in self.__pacientes:
            print(p.obtener_info())

    @property
    def total_pacientes(self):
        return len(self.__pacientes)

    @property
    def total_citas(self):
        return len(self.__citas)

    def agregar_medico(self, medico):
        self.__medicos.append(medico)

    @property
    def medicos(self):
        return self.__medicos

    def programar_cita(self, cita):
        self.__citas.append(cita)
        cita._Cita__medico.agregar_cita(cita)

    def mostrar_citas(self):
        if not self.__citas:
            print("No hay citas programadas.")
            return

        for c in self.__citas:
            print(c.mostrar())

    def leer_fecha(self, mensaje):
        while True:
            try:
                fecha_str = input(mensaje)
                return datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                print("Formato inválido. Use YYYY-MM-DD (ejemplo: 2001-05-10)")

    def leer_hora(self, mensaje):
        while True:
            try:
                hora_str = input(mensaje)
                return datetime.strptime(hora_str, "%H:%M").time()
            except ValueError:
                print("Formato inválido. Use HH:MM (ejemplo: 14:30)")

    def leer_opcion(self, mensaje, opciones_validas):
        while True:
            opcion = input(mensaje).strip()
            if opcion in opciones_validas:
                return opcion
            print(f"Opción inválida. Elija entre: {', '.join(opciones_validas)}")

    def ejecutar_menu(self):
        print("\n" + "=" * 40)
        print(" SISTEMA DE GESTIÓN CLÍNICA - CLINISOFT")
        print("    Clínica Marbella - Versión 2.4")
        print("=" * 40)

        opciones_menu = ["1", "2", "3", "4", "5", "6", "7", "8"]

        while True:

            print("           MENÚ PRINCIPAL")
            print("=" * 40)
            print("1. Registrar paciente")
            print("2. Buscar paciente por DNI")
            print("3. Buscar paciente por nombre")
            print("4. Ver todos los pacientes")
            print("5. Ver métricas de la clínica")
            print("6. Programar cita médica")
            print("7. Actualizar datos de paciente")
            print("8. Salir")
            print("=" * 40)

            op = self.leer_opcion("Seleccione una opción: ", opciones_menu)

            if op == "1":
                print("\n--- REGISTRO DE PACIENTE ---")
                try:
                    dni = input("DNI: ").strip()
                    if not dni.isdigit() or len(dni) != 8:
                        print("Error: el DNI debe tener 8 dígitos numéricos")
                        continue

                    nombre = input("Nombre: ").strip()
                    apellido = input("Apellido: ").strip()
                    telefono = input("Teléfono: ").strip()
                    fecha = self.leer_fecha("Fecha Nacimiento (YYYY-MM-DD): ")

                    if fecha > date.today():
                        print("Error: La fecha de nacimiento no puede ser futura")
                        continue

                    p = Paciente(dni, nombre, apellido, telefono, fecha)

                    if self.registrar_paciente(p):
                        print("Registro exitoso: El paciente ha sido registrado correctamente")
                    else:
                        print("Error: El paciente ya existe con ese DNI")

                except Exception as e:
                    print(f"Error al registrar paciente: {e}")

            elif op == "2":
                print("\n--- BUSCAR PACIENTE POR DNI ---")
                try:
                    dni = input("DNI del paciente: ").strip()
                    p = self.buscar_paciente_dni(dni)

                    if p:
                        print("\nPaciente encontrado:")
                        print(p.obtener_info())
                    else:
                        print("Error: paciente no encontrado")

                except Exception as e:
                    print(f"Error en la búsqueda: {e}")

            elif op == "3":
                print("\n--- BUSCAR PACIENTE POR NOMBRE ---")
                try:
                    nombre = input("Nombre a buscar: ").strip()
                    lista = self.buscar_paciente_nombre(nombre)

                    if lista:
                        print(f"\n Se encontraron {len(lista)} paciente(s):")
                        for p in lista:
                            print(p.obtener_info())
                    else:
                        print(" No se encontraron pacientes con ese nombre")

                except Exception as e:
                    print(f" Error en la búsqueda: {e}")

            elif op == "4":
                print("\n--- LISTA DE TODOS LOS PACIENTES ---")
                try:
                    self.mostrar_pacientes()
                except Exception as e:
                    print(f" Error al mostrar pacientes: {e}")

            elif op == "5":
                print("\n--- MÉTRICAS DE LA CLÍNICA ---")
                try:
                    print(f"Total de pacientes: {self.total_pacientes}")
                    print(f"Total de citas: {self.total_citas}")

                    if self.medicos:
                        print(f"Total de médicos: {len(self.medicos)}")
                        print("\nMédicos activos:")
                        for m in self.medicos:
                            print(f"  • Dr. {m.nombre_completo} - {m.especialidad} ({m.total_citas} citas)")

                except Exception as e:
                    print(f" Error al mostrar métricas: {e}")

            elif op == "6":
                print("\n--- PROGRAMAR CITA MÉDICA ---")
                try:
                    dni = input("DNI del paciente: ").strip()
                    p = self.buscar_paciente_dni(dni)

                    if p:
                        print(f" Paciente: {p.nombre_completo}")

                        if not self.medicos:
                            print(" No hay médicos disponibles")
                            continue

                        print("\nMédicos disponibles:")
                        for i, m in enumerate(self.medicos, 1):
                            print(f"{i}. Dr. {m.nombre_completo} - {m.especialidad}")

                        opciones_medicos = [str(i) for i in range(1, len(self.medicos) + 1)]
                        opcion_medico = self.leer_opcion("Seleccione el médico (número): ", opciones_medicos)
                        medico_seleccionado = self.medicos[int(opcion_medico) - 1]

                        print(f"\n Especialidad seleccionada: {medico_seleccionado.especialidad}")

                        fecha = self.leer_fecha("Fecha de la cita (YYYY-MM-DD): ")

                        if fecha < date.today():
                            print(" No se pueden programar citas en fechas pasadas")
                            continue

                        hora = self.leer_hora("Hora de la cita (HH:MM): ")

                        codigo = "C" + datetime.now().strftime("%Y%m%d%H%M%S")
                        cita = Cita(codigo, p, medico_seleccionado, fecha, hora)

                        self.programar_cita(cita)
                        print(f" Cita programada correctamente")
                        print(f"   Código: {codigo}")
                        print(f"   Especialidad: {medico_seleccionado.especialidad}")
                        print(f"   Médico: Dr. {medico_seleccionado.nombre_completo}")
                    else:
                        print(" Paciente no encontrado")

                except Exception as e:
                    print(f" Error al programar cita: {e}")

            elif op == "7":
                print("\n--- ACTUALIZAR DATOS DE PACIENTE ---")
                try:
                    dni = input("DNI del paciente a actualizar: ").strip()
                    p = self.buscar_paciente_dni(dni)

                    if p:
                        print(f"\n Paciente actual: {p.obtener_info()}")
                        print("\n¿Qué desea actualizar?")
                        print("1. Teléfono")
                        print("2. Cancelar")

                        sub_op = self.leer_opcion("Seleccione: ", ["1", "2"])

                        if sub_op == "1":
                            nuevo_tel = input("Nuevo teléfono: ").strip()
                            try:
                                p.telefono = nuevo_tel
                                print(" Teléfono actualizado correctamente")
                            except ValueError as e:
                                print(f" {e}")
                    else:
                        print(" Paciente no encontrado")

                except Exception as e:
                    print(f" Error al actualizar: {e}")

            elif op == "8":
                print("\n" + "=" * 50)
                print("   Gracias por usar CliniSoft")
                print("   ¡Hasta pronto!")
                print("=" * 50 + "\n")
                break

# Función principal
def menu():
    clinica = Clinica("Clínica Marbella")

    # Médicos según su especialidad
    medico1 = Medico("40123456", "Carlos", "García Perales", "987654321", "Medicina Interna")
    medico2 = Medico("41234567", "María", "López Perez", "976543210", "Urología")
    medico3 = Medico("42345678", "Roberto", "Sánchez Hinostroza", "965432109", "Cardiología")
    medico4 = Medico("43456789", "Luisa", "Fernández Gómez", "954321098", "Traumatología")
    medico5 = Medico("44567890", "Ana Bárbara", "Martínez Ruiz", "943210987", "Cirugía Torácica")

    clinica.agregar_medico(medico1)
    clinica.agregar_medico(medico2)
    clinica.agregar_medico(medico3)
    clinica.agregar_medico(medico4)
    clinica.agregar_medico(medico5)

    clinica.ejecutar_menu()


if __name__ == "__main__":
    menu()
