from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Alumno,Genero

from .forms import GeneroForm

# Create your views here.
class persona:
    def __init__(self, nombre, edad):
        self.nombre=nombre
        self.edad=edad
        super().__init__()


def index(request):
    hijo=persona("Juan Perez", "7")

    lista=["Lazaña", "Charquican", "Porotos granado"]

    alumnos= Alumno.objects.all()


    context={"hijo":hijo, "nombre":"Claudia Andrea", "comidas":lista, "alumnos":alumnos }

    return render(request, 'alumnos/index.html', context)
def crud(request):
    alumnos = Alumno.objects.all()
    context = {'alumnos': alumnos}
    return render(request,'alumnos/alumnos_list.html', context)

def alumnosAdd(request):
    if request.method != 'POST':

        generos = Genero.objects.all()
        context = {'generos': generos}
        return render(request, 'alumnos/alumnos_add.html', context)
    elif request.method == 'POST':

        rut=request.POST['rut']
        nombre=request.POST['nombre']
        aPaterno=request.POST['paterno']
        aMaterno=request.POST['materno']
        fechaNac=request.POST['fechaNac']
        genero=request.POST['genero']
        telefono=request.POST['telefono']
        email=request.POST['email']
        direccion=request.POST['direccion']
        activo="1"

        objGenero = Genero.objects.get(id_genero = genero)
        obj=Alumno.objects.create(  rut=rut, 
                                    nombre=nombre, 
                                    apellido_paterno=aPaterno, 
                                    apellido_materno=aMaterno, 
                                    fecha_nacimiento=fechaNac, 
                                    id_genero=objGenero, 
                                    telefono=telefono, 
                                    email=email, 
                                    direccion=direccion, 
                                    activo=1)
        obj.save()
        context = {'mensaje': 'Ok, datos guardados...'}
        return render(request, 'alumnos/alumnos_add.html', context)

def alumnos_del(request, pk):
    context = {}
    try:
        alumno = Alumno.objects.get(rut=pk)

        alumno.delete()
        mensaje = 'Ok, registro eliminado...'
        alumnos = Alumno.objects.all()
        context = {'alumnos': alumnos, 'mensaje': mensaje}
        return render(request, 'alumnos/alumnos_list.html', context)
    except:
        mensaje='Error, rut no existe...'
        alumnos = Alumno.objects.all()
        context = {'alumnos': alumnos, 'mensaje': mensaje}
        return render(request, 'alumnos/alumnos_list.html', context)
    
def alumnos_findEdit(request, pk):

    if pk != "":
        alumno = Alumno.objects.get(rut=pk)
        generos = Genero.objects.all()

        print(type(alumno.id_genero.genero))

        context = {'alumno': alumno, 'generos': generos}
        if alumno:
            return render(request, 'alumnos/alumnos_edit.html', context)
        else:
            context={'mensaje':'Error, rut no existe...'}
        return render(request, 'alumnos/alumnos_list.html', context)
    
def alumnosUpdate(request):

    if request.method == "POST":
        
        rut=request.POST['rut']
        nombre=request.POST['nombre']
        aPaterno=request.POST['paterno']
        aMaterno=request.POST['materno']
        fechaNac=request.POST['fechaNac']
        genero=request.POST['genero']
        telefono=request.POST['telefono']
        email=request.POST['email']
        direccion=request.POST['direccion']
        activo="1"

        objGenero = Genero.objects.get(id_genero = genero)

        alumno =Alumno()
        alumno.rut=rut
        alumno.nombre=nombre
        alumno.apellido_paterno=aPaterno
        alumno.apellido_materno=aMaterno
        alumno.fecha_nacimiento=fechaNac
        alumno.id_genero=objGenero
        alumno.telefono=telefono
        alumno.email=email
        alumno.direccion=direccion
        alumno.activo=1
        alumno.save()
        
        generos=Genero.objects.all()
        context = {'generos': generos, 'mensaje': 'Ok, datos actualizados...', 'alumno': alumno}
        return render(request, 'alumnos/alumnos_edit.html', context)
    else:
        alumnos = Alumno.objects.all()
        context = {'alumnos': alumnos}
        return render(request, 'alumnos/alumnos_list.html', context) 

def crud_generos(request):
    generos = Genero.objects.all()
    context = {'generos': generos}
    print("enviando datos generos_list")
    return render(request,'alumnos/generos_list.html', context) 


def generosAdd(request):

    print("estoy en controlador generosAdd")
    context = {}

    if request.method == 'POST':
        print("controlador es un post...")
        form = GeneroForm(request.POST)
        if form.is_valid():
            print("estoy en agregar, is_valid...")
            form.save()

            form = GeneroForm()
            context = {'mensaje': 'Ok, datos guardados...', 'form': form}
            return render(request, 'alumnos/generos_add.html', context)
        
    else:
        form = GeneroForm()
        context = {'form': form}
        return render(request, 'alumnos/generos_add.html', context)

def generos_del(request, pk):
    mensajes= []
    errores = []
    generos = Genero.objects.all()  
    try:
        genero = Genero.objects.get(id_genero=pk)
        context={}
        if genero:
            genero.delete()
            mensajes.append('Bien, datos eliminado...')
            context = {'generos': generos, 'mensaje': mensaje, 'errores': errores}
            return render(request, 'alumnos/generos_list.html', context)
    except:
        print('Error, id no existe...')
        generos = Genero.objects.all()
        mensaje="Error, id no existe..."
        context = {'generos': generos, 'mensaje': mensaje}
        return render(request, 'alumnos/generos_list.html', context)
    
def generos_edit(request, pk):
    try:
        genero=Genero.objects.get(id_genero=pk)
        context={}
        if genero:
            print("edit encontró el genero...")
            if request.method == 'POST':
                print("edit es un post...")
                form = GeneroForm(request.POST, instance=genero)
                form.save()
                mensaje = "bie, datos actualizados..."
                context = {'genero': genero, 'form': form 'mensaje': mensaje}
                return render(request, 'alumnos/generos_edit.html', context)
    except:
        print("Error, id no existe...")
        generos = Genero.objects.all()
        mensaje = "Error, id no existe..."
        context = {'generos': generos, 'mensaje': mensaje}
        return render(request, 'alumnos/generos_list.html', context)

def generos_edit(request, pk):
    try:
        genero=Genero.objects.get(id_genero=pk)
        context={}
        if genero:
            print("Edit encontró el genero...")
            if request.method == 'POST':
                print("edit es un POST")
                form = GeneroForm(request.POST, instance=genero)
                form.save()
                mensaje = "bie, datos actualizados..."
                print(mensaje)
                context = {'genero': genero, 'form': form 'mensaje': mensaje}
                return render(request, 'alumnos/generos_edit.html', context)
            else:
                print("edit, no es un POST...")
                form = GeneroForm(instance=genero)
                mensaje=""
                context = {'genero': genero, 'form': form, 'mensaje': mensaje}
                return render(request, 'alumnos/generos_edit.html', context)
    except:
        print("Error, id no existe...")
        generos = Genero.objects.all()
        mensaje = "Error, id no existe..."
        context = {'generos': generos, 'mensaje': mensaje}
        return render(request, 'alumnos/generos_list.html', context)
 
        


        
