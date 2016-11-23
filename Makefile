all: project2.o

project2.o: project2.cpp
	g++ project2.cpp -o project2.o -fopenmp

clean:
	rm -f project2.o
