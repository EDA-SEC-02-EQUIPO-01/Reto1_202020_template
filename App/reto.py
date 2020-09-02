"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv

from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt
from Sorting import mergesort as mr
from Sorting import shellsort as sh

from time import process_time 



def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
    print("6- Crear ranking")
    print("0- Salir")




def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1



def loadCSVFile (file, cmpfunction):
    lst=lt.newList("ARRAY_LIST", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter=";"
    try:
        with open(  cf.data_dir + file, encoding="utf-8") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
    except:
        print("Hubo un error con la carga del archivo")
    return lst


def loadMovies ():
    lst = loadCSVFile("theMoviesdb/SmallMoviesDetailsCleaned.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst
def loadCasting ():
    lst = loadCSVFile("theMoviesdb/MoviesCastingRaw-small.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def less(item1,item2,etiqueta="vote_average"):
    if float(item1[etiqueta])<float(item2[etiqueta]):
        return True
    return False
def greater(item1,item2,etiqueta="vote_average"):
    if float(item1[etiqueta])>float(item2[etiqueta]):
        return True
    return False
def less_count(item1,item2,etiqueta="vote_count"):
    if int(item1[etiqueta])<int(item2[etiqueta]):
        return True
    return False
def greater_count(item1,item2,etiqueta="vote_count"):
    if int(item1[etiqueta])>int(item2[etiqueta]):
        return True
    return False
def promediar(lst,caracteristica):
    total=0
    for i in range(lt.size(lst)):
        total+=float(lst['elements'][i][caracteristica])
    return round((total/lt.size(lst)),1)

def CrearRankingPelicula(calificacion, lst, orden,rango=10,seguro=False):
    """
    Retorna una lista con cierta cantidad de elementos ordenados por el criterio
    """
    if lst['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter={}
        almacen={}
        if calificacion.lower()=="peor":
            if orden==0:
                mr.mergesort(lst,less_count)
                for i in range(1,rango+1):
                    counter=lt.getElement(lst,i)
                    if not seguro:    
                        print(f"{counter['title']}:{counter['vote_count']}")
                    almacen[counter['title']]=counter['vote_count']
            else:    
                mr.mergesort(lst,less)
                for f in range(1,rango+1):
                    counter=lt.getElement(lst,f)
                    if not seguro:
                        print(f"{counter['title']}:{counter['vote_average']}")
                    almacen[counter['title']]=counter['vote_count']
        elif calificacion.lower()=="mejor":
            if orden==0:
                mr.mergesort(lst,greater_count)
                for i in range(1,rango+1):
                    counter=lt.getElement(lst,i)
                    if not seguro:
                        print(f"{counter['title']}:{counter['vote_count']}")
                    almacen[counter['title']]=counter['vote_count']
            else:    
                mr.mergesort(lst,greater)
                for i in range(1,rango+1):
                    counter=lt.getElement(lst,i)
                    if not seguro:
                        print(f"{counter['title']}:{counter['vote_average']}")
                    almacen[counter['title']]=counter['vote_count']
        t1_stop=process_time()
        
        print(f"tiempo de ejecucion: {t1_stop-t1_start} segundos")
        return almacen

def conversor_entre_cvs(id_movie,iterador):
    while it.hasNext(iterador):
        counter=it.next(iterador)
        if counter['id']==id_movie:
            return counter

def conocer_un_director(lst,lst2, director,etiqueta="director_name",criterio_calificacion="vote_average"):
    if lst['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        coleccion=lt.newList("ARRAY_LIST")
        iterador_coleccion=it.newIterator(lst)
        while it.hasNext(iterador_coleccion):
            counter=it.next(iterador_coleccion)
            if director.lower() in counter[etiqueta].lower():
                id_store=counter['id']
                iterador_pelicula=it.newIterator(lst2)
                pelicula_convertida=conversor_entre_cvs(id_store,iterador_pelicula)
                lt.addLast(coleccion,pelicula_convertida)
                print(lt.lastElement(coleccion)['title'])
        promedio=promediar(coleccion,criterio_calificacion)
        t1_stop=process_time()  
        print(f"tiempo de ejecucion: {t1_stop-t1_start} segundos")
        print(f"Peliculas totales:{lt.size(coleccion)}\nCalificacion promedio:{promedio}")
        
def GetMoviesByActor (lstactors,actorname,lstmovies):
    if lstactors["size"] == 0:
        print ("La lista está vacía")
        return 0
    else:
        movies=lt.newList("ARRAY_LIST")
        col={}
        itcast = it.newIterator(lstactors)
        while it.hasNext(itcast):
            counter=it.next(itcast)
            if counter["actor1_name"].lower() == actorname.lower():
                ids=counter["id"]
                itmovies=it.newIterator(lstmovies)
                movie= conversor_entre_cvs(ids,itmovies)
                lt.addLast(movies,movie)
                print(lt.lastElement(movies)["original_title"])
                dire=counter["director_name"]
                if dire in col:
                    col[dire]+=1
                else:
                    col[dire]=1
            if counter["actor2_name"].lower() == actorname.lower():
                ids=counter["id"]
                itmovies=it.newIterator(lstmovies)
                movie= conversor_entre_cvs(ids,itmovies)
                lt.addLast(movies,movie)
                print(lt.lastElement(movies)["original_title"])
                dire=counter["director_name"]
                if dire in col:
                    col[dire]+=1
                else:
                    col[dire]=1
            if counter["actor3_name"].lower() == actorname.lower():
                ids=counter["id"]
                itmovies=it.newIterator(lstmovies)
                movie= conversor_entre_cvs(ids,itmovies)
                lt.addLast(movies,movie)
                print(lt.lastElement(movies)["original_title"])
                dire=counter["director_name"]
                if dire in col:
                    col[dire]+=1
                else:
                    col[dire]=1
            if counter["actor4_name"].lower() == actorname.lower():
                ids=counter["id"]
                itmovies=it.newIterator(lstmovies)
                movie= conversor_entre_cvs(ids,itmovies)
                lt.addLast(movies,movie)
                print(lt.lastElement(movies)["original_title"])
                dire=counter["director_name"]
                if dire in col:
                    col[dire]+=1
                else:
                    col[dire]=1
            if counter["actor5_name"].lower() == actorname.lower():
                ids=counter["id"]
                itmovies=it.newIterator(lstmovies)
                movie= conversor_entre_cvs(ids,itmovies)
                lt.addLast(movies,movie)
                print(lt.lastElement(movies)["original_title"])
                dire=counter["director_name"]
                if dire in col:
                    col[dire]+=1
                else:
                    col[dire]=1
    promedio= promediar(movies,"vote_average")
    ordenado= sorted(col.items(),key=lambda x:x[1], reverse=True)
    print (f"peliculas totales: {lt.size(movies)}\nCalificación promedio: {promedio}\nDirector con más colaboraciones: {ordenado[0][0]}")

def conocer_un_genero(lst,director,seguro=False):
    if lst['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        coleccion=lt.newList("ARRAY_LIST")
        iterador_coleccion=it.newIterator(lst)
        while it.hasNext(iterador_coleccion):
            counter=it.next(iterador_coleccion)
            if director.lower() in counter["genres"].lower():
                lt.addLast(coleccion,counter)
                if not seguro:
                    print(lt.lastElement(coleccion)['title'])
        promedio=promediar(coleccion,"vote_count")
        t1_stop=process_time()
        
        print(f"tiempo de ejecucion: {t1_stop-t1_start} segundos")
        print(f"Peliculas totales:{lt.size(coleccion)}\nCalificacion promedio:{promedio}")
    return coleccion

def ranking_de_genero(lst,genero,criterio,ordenamiento,num):
    if lst['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        lista_genero=conocer_un_genero(lst,genero,True)
        lista_ordenada_genero=CrearRankingPelicula(criterio,lista_genero,ordenamiento,num,True)
        if criterio=="mejor":
            if ordenamiento==0:
                print(f"{num} BEST COUNTS MOVIES!!\n{lista_ordenada_genero}")
            elif ordenamiento==1:
                print(f"{num} BEST AVERAGE MOVIES!!\n{lista_ordenada_genero}")
        elif criterio=="peor":
            if ordenamiento==0:
                print(f"{num} WORST COUNTS MOVIES!!\n{lista_ordenada_genero}")
            elif ordenamiento==1:
                print(f"{num} WORST AVERAGE MOVIES!!\n{lista_ordenada_genero}")
    t1_stop=process_time()
    print(f"tiempo de ejecucion: {t1_stop-t1_start} segundos")


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:

            if int(inputs[0])==1: #opcion 1
                lstmovies = loadMovies()
                lstcasting=loadCasting()

            elif int(inputs[0])==2: #opcion 2
                orden=int(input("Ingrese 0 para ordenar segun numero de votos\nIngrese 1 para ordenar segun calificacion promedio\n"))
                criterio=input("Ingrese 'mejor'(sin comillas) para ranking de mejores peliculas\nIngrese 'peor'(sin comillas) para ranking de peores peliculas\n")
                CrearRankingPelicula(criterio,lstmovies,orden)

            elif int(inputs[0])==3: #opcion 3
                director=input("Ingrese el nombre del director a buscar\n")
                conocer_un_director(lstcasting,lstmovies,director)

            elif int(inputs[0])==4: #opcion 4
                actorname= input("Ingrese el actor que desea conocer: ")
                GetMoviesByActor(lstcasting,actorname,lstmovies)

            elif int(inputs[0])==5: #opcion 5
                genero=input("Ingrese el genero que desea entender\n")
                conocer_un_genero(lstmovies,genero)
            elif int(inputs[0])==6: #opcion 6
                genero=input("Ingrese el genero que desea un ranking\n")
                orden=int(input("Ingrese 0 para ordenar segun numero de votos\nIngrese 1 para ordenar segun calificacion promedio\n"))
                criterio=input("Ingrese 'mejor'(sin comillas) para ranking de mejores peliculas\nIngrese 'peor'(sin comillas) para ranking de peores peliculas\n")
                num=int(input("Ingrese el numero de peliculas que desea ver en el ranking\n"))
                ranking_de_genero(lstmovies,genero,criterio,orden,num)

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()
