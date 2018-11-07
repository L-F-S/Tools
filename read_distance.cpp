#include <iostream>
#include <fstream>
#include <cstdlib>
#include <math.h>
#include <iomanip>
#include <limits>
#include <time.h>
#include <stdio.h>      
#include <stdlib.h>     

#define S_c (10)
#define cutoff (2.0)

using namespace std;

long double x[1000], y[1000], z[1000], vx[1000], vy[1000], vz[1000], d[1000][1000];
long double delx1, dely1, delz1;




ofstream DIS("Distance.dat");

int main (int argc, char *argv[])
{
  int i=0, j = 0; 
  ifstream fin (argv[1]); 
  std::string qlline;
  string param;
  int beads=0;


  if (argc < 2 )
    {
      cout << "Insert the input file and elastic constants" << endl; 
      return 1; 
    }

  while (std::getline(fin, qlline))
  {  
    if (qlline.find("#Coordinates") != 0) {continue;}
             
    if(fin.fail()) 
      { 
      	cout << "error" << endl; 
      	return 1; 
      }

    while(!fin.eof()) 
      {
	      fin >> x[j]; 
      	fin >> y[j]; 
      	fin >> z[j]; 
      	fin >> vx[j]; 
	      fin >> vy[j]; 
	      fin >> vz[j]; 
      	++j; 
      }  
  }

  ifstream fin_1 (argv[1]); 
  while (getline(fin_1, qlline)) {
  if (qlline.find("#read_chain") != 0) {continue;}

  
           fin_1 >> param;
      	   fin_1 >> beads;   
 
     }
  fin_1.close(); 

  if (beads > 1000)
   {
        cout << "The number of beads are larger than the array size" << endl; 
	return 1; 
    }


 
   
     //DIS<< "bead' index" <<
    //setw(25)<< "neighbour' index" <<
    //setw(25)<< "distance" <<endl;

 
 for ( i=0; i<beads-1; i++)
    { 
       for ( j=i+1+S_c; j<beads; j++)
         {
          
    	  delx1 = x[i] - x[j];      
     	  dely1 = y[i] - y[j];
    	  delz1 = z[i] - z[j];

          d[i][j] = sqrt(delx1*delx1 + dely1*dely1 + delz1*delz1);

             if (d[i][j]<cutoff)
              {
                DIS<<setw(3)<<i<<
	              setw(30)<<j<<
	              setw(25)<<d[i][j]<<endl;
              }
         }
    }


  fin.close(); 

  return 0; 
}






