from datetime import datetime, date, time


class Persona:
    def __init__(self, id, nombre, apellido, telefono):
        self._id = id
        self._nombre = nombre
        self._apellido = apellido
        self._telefono = telefono

    def get_id(self):
        return self._id

    def get_nombre_completo(self):
        return self._nombre + " " + self._apellido


class Paciente(Persona):
    def __init__(self, id, nombre, apellido, telefono, fecha_nacimiento):
        super().__init__(id, nombre, apellido, telefono)
        self._fecha_nacimiento = fecha_nacimiento

    def obtener_info(self):
        hoy = date.today()
        edad = hoy.year - self._fecha_nacimiento.year - ((hoy.month, hoy.day) < (self._fecha_nacimiento.month, self._fecha_nacimiento.day))
        return self._id + " | " + self.get_nombre_completo() + " | Edad: " + str(edad)


class Medico(Persona):
    def __init__(self, id, nombre, apellido, telefono, especialidad):
        super().__init__(id, nombre, apellido, telefono)
        self._especialidad = especialidad
        self._citas = []

    def agregar_cita(self, cita):
        self._citas.append(cita)

    def get_especialidad(self):
        return self._especialidad


class Cita:
    def __init__(self, codigo, paciente, medico, fecha, hora):
        self._codigo = codigo
        self._paciente = paciente
        self._medico = medico
        self._fecha = fecha
        self._hora = hora

    def mostrar(self):
        return (self._codigo + " | " +
                self._paciente.get_nombre_completo() + " | " +
                self._medico.get_nombre_completo() + " | " +
                str(self._fecha) + " " + self._hora.strftime("%H:%M"))


class Clinica:
    def __init__(self, nombre):
        self._nombre = nombre
        self._pacientes = []
        self._medicos = []
        self._citas = []

    def registrar_paciente(self, paciente):
        for p in self._pacientes:
            if p.get_id() == paciente.get_id():
                return False
        self._pacientes.append(paciente)
        return True

    def buscar_paciente_id(self, id):
        for p in self._pacientes:
            if p.get_id() == id:
                return p
        return None

    def buscar_paciente_nombre(self, nombre):
        encontrados = []
        for p in self._pacientes:
            if nombre.lower() in p.get_nombre_completo().lower():
                encontrados.append(p)
        return encontrados

    def mostrar_pacientes(self):
        for p in self._pacientes:
            print(p.obtener_info())

    def total_pacientes(self):
        return len(self._pacientes)

    def total_citas(self):
        return len(self._citas)

    def agregar_medico(self, medico):
        self._medicos.append(medico)

    def programar_cita(self, cita):
        self._citas.append(cita)
        cita._medico.agregar_cita(cita)

    def mostrar_citas(self):
        for c in self._citas:
            print(c.mostrar())


def demostrar_sistema(clinica):
    print("\n=== DEMOSTRACIÓN AUTOMÁTICA ===\n")

    p1 = Paciente("P001", "Juan", "Perez", "999111222", date(2000, 5, 10))
    p2 = Paciente("P002", "Ana", "Torres", "988222333", date(1999, 3, 20))

    clinica.registrar_paciente(p1)
    clinica.registrar_paciente(p2)

    fecha = date.today()
    hora = time(10, 0)

    c1 = Cita("C001", p1, clinica._medicos[0], fecha, hora)
    clinica.programar_cita(c1)

    print("Pacientes registrados automáticamente:")
    clinica.mostrar_pacientes()

    print("\nCitas registradas automáticamente:")
    clinica.mostrar_citas()


def menu():
    clinica = Clinica("Clínica Marbella")

    medico = Medico("M001", "Carlos", "García", "987654321", "Medicina General")
    clinica.agregar_medico(medico)

    print("Bienvenido al Sistema de Gestión Clínica CliniSoft")
    print("Desarrollado para la Clínica Marbella")
    print("=" * 50)

    demo = input("¿Desea ver la demostración automática? (s/n): ").lower()
    if demo == "s":
        demostrar_sistema(clinica)

    while True:
        print("\n=== MENÚ CLINISOFT ===")
        print("1. Registrar paciente")
        print("2. Buscar paciente por ID")
        print("3. Buscar paciente por nombre")
        print("4. Ver todos los pacientes")
        print("5. Ver métricas de la clínica")
        print("6. Programar cita médica")
        print("7. Demostrar funcionalidades completas")
        print("8. Salir")

        op = input("Seleccione una opción: ")

        if op == "1":
            id = input("ID: ")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            telefono = input("Teléfono: ")
            fecha = datetime.strptime(input("Fecha Nacimiento (YYYY-MM-DD): "), "%Y-%m-%d").date()

            p = Paciente(id, nombre, apellido, telefono, fecha)

            if clinica.registrar_paciente(p):
                print("Paciente registrado correctamente")
            else:
                print("El paciente ya existe")

        elif op == "2":
            id = input("ID del paciente: ")
            p = clinica.buscar_paciente_id(id)
            if p:
                print(p.obtener_info())
            else:
                print("Paciente no encontrado")

        elif op == "3":
            nombre = input("Nombre a buscar: ")
            lista = clinica.buscar_paciente_nombre(nombre)
            for p in lista:
                print(p.obtener_info())

        elif op == "4":
            clinica.mostrar_pacientes()

        elif op == "5":
            print("Total de pacientes:", clinica.total_pacientes())
            print("Total de citas:", clinica.total_citas())

        elif op == "6":
            id = input("ID del paciente: ")
            p = clinica.buscar_paciente_id(id)

            if p:
                fecha = datetime.strptime(input("Fecha (YYYY-MM-DD): "), "%Y-%m-%d").date()
                hora = datetime.strptime(input("Hora (HH:MM): "), "%H:%M").time()

                codigo = "C" + datetime.now().strftime("%H%M%S")
                cita = Cita(codigo, p, clinica._medicos[0], fecha, hora)

                clinica.programar_cita(cita)
                print("Cita programada correctamente")

            else:
                print("Paciente no existe")

        elif op == "7":
            demostrar_sistema(clinica)

        elif op == "8":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida")


menu()
