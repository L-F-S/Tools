#include <iostream>
#include <fstream>
#include <cstdlib>
#include <math.h>
#include <iomanip>
#include <limits>
#include <time.h>
#include <stdio.h>      
#include <stdlib.h>     


#define LOW_elastic_limit (5)
#define UP_elastic_limit (150)

using namespace std;
long double x[1000], y[1000], z[1000], vx[1000], vy[1000], vz[1000], v[100], c[100];
long double delx1, dely1, delz1, delx2, dely2, delz2, delx3, dely3, delz3;
long double d1, d2, D, f, T, F, dn1, dn2, sgn, a, b, p, a1, b1;
long double xcurl1, ycurl1, zcurl1, xcurl2, ycurl2, zcurl2, xcurl3, ycurl3, zcurl3;
long double theta[1000-1], phi[1000-1], kb[1000-1], kt1[1000-1], kt2[1000-1];
int NB;

ofstream angle("forcefield.dat");

int main (int argc, char *argv[])
{
  int i=0, j = 0; 
  ifstream fin (argv[1]); 
  std::string qlline;
  string param;
  int beads=0;
  int BLOCKSIZE=1;


  if (argc < 6 )
    {
      cout << "Insert the input file, elastic constants, and blocksize" << endl; 
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
    //cout<<param<<"\t"<<beads<<endl;
    //printf("%d\n",beads);
  }
  fin_1.close(); 
  
  if (beads > 1000)
    {
      cout << "The number of beads are larger than the array size" << endl; 
      return 1; 
    }


 
  for (int k=0; k<beads-2; k++)
    {
      theta[k] = 0;
      phi[k] = 0;
    }
  
  for (int j=0; j<beads-2; j++)
    {

      delx1 = x[j] - x[j+1];      
      dely1 = y[j] - y[j+1];
      delz1 = z[j] - z[j+1];

      delx2 = x[j+1] - x[j+2];      
      dely2 = y[j+1] - y[j+2];
      delz2 = z[j+1] - z[j+2];    
    
      d1 = sqrt(delx1*delx1 + dely1*dely1 + delz1*delz1);
      d2 = sqrt(delx2*delx2 + dely2*dely2 + delz2*delz2);
                     
      D = - (delx1*delx2 + dely1*dely2 + delz1*delz2)/(d1*d2);
      theta[j] = acos(D);
      // cout<<d1<<endl;
    }

  for (int j=0; j<beads-3; j++)
    {
        
      delx1 = x[j] - x[j+1];
      delx2 = x[j+1] - x[j+2];
      delx3 = x[j+2] - x[j+3];

      dely1 = y[j] - y[j+1];
      dely2 = y[j+1] - y[j+2];
      dely3 = y[j+2] - y[j+3];

      delz1 = z[j] - z[j+1];
      delz2 = z[j+1] - z[j+2];
      delz3 = z[j+2] - z[j+3];

      xcurl1 = dely1*delz2 - dely2*delz1;
      ycurl1 = delz1*delx2 - delz2*delx1;
      zcurl1 = delx1*dely2 - delx2*dely1;

      xcurl2 = dely2*delz3 - dely3*delz2;
      ycurl2 = delz2*delx3 - delz3*delx2;
      zcurl2 = delx2*dely3 - delx3*dely2;

      dn1 = sqrt(xcurl1*xcurl1 + ycurl1*ycurl1 + zcurl1*zcurl1);
      dn2 = sqrt(xcurl2*xcurl2 + ycurl2*ycurl2 + zcurl2*zcurl2);

      T = (xcurl1*xcurl2 + ycurl1*ycurl2 + zcurl1*zcurl2)/(dn1*dn2);

      xcurl3 = ycurl1*zcurl2 - zcurl1*ycurl2;
      ycurl3 = zcurl1*xcurl2 - xcurl1*zcurl2;
      zcurl3 = xcurl1*ycurl2 - ycurl1*xcurl2;

      sgn = (xcurl3*delx2 + ycurl3*dely2 + zcurl3*delz2);
      sgn = -sgn/sqrt(sgn*sgn);
      phi[j] = sgn*acos(T);
    }

  a =  atof(argv[2]);
  b =  atof(argv[3]);
  p =  atof(argv[4]);
  BLOCKSIZE = atoi(argv[5]);
  NB = (int) (floor((beads-2.)/(1.*BLOCKSIZE)));
  srand (time(NULL));
  for (int i=1; i<NB+2; i++)
    {        
      v[i] = (rand()%1000);
      v[i] = v[i]/1000;
    }

  if(p == 0) // for p=0 we have even elastic parameters distribution
    {
      for (int k=0; k<beads-2; k++) 
	{
	  kb[k] = a;
	  kt1[k] = b;
	  //kt2[k] = c;
	}   
    }
  else
    {
         
      for (int k=1; k<NB+2; k++) 
	{    
	  a1 = 0;
	  b1 = 0;

	  a1 = a + v[k]*5.0;
	  b1 = b + v[k]*5.0;
	  //kt2[k] = c;
	  //printf("%d\t%g\t%d\t%d\t%d\n",k,v[k],NB,beads,BLOCKSIZE);
	  if(a1 < LOW_elastic_limit) a1 = LOW_elastic_limit;
	  if(b1 < LOW_elastic_limit) b1 = LOW_elastic_limit;
	  if(a1 > UP_elastic_limit) a1 = UP_elastic_limit;
	  if(b1 > UP_elastic_limit) b1 = UP_elastic_limit;

	  for(int j=0; j<BLOCKSIZE; j++) 
	    {
	      j = (k-1)*BLOCKSIZE + j;
	      kb[j] = a1;
	      kt1[j] = b1;
	      //kt2[j] = c;
	      j = j - (k-1)*BLOCKSIZE;
	    }
                
	}  
    } 


  angle<<"#Elastic parameters"<<
    setw(14)<< "kb" <<
    setw(15)<< "theta" <<
    setw(10)<< "kt1" <<
    setw(10)<< "kt2" <<
    setw(15)<< "phi" <<endl;
            
  angle<<"#atom"<<endl;
 
  

  for (int k=0; k<beads-2; k++)
    {
      if (k==beads-3){kt1[k] = 0.0; kt2[k] = 0.0; phi[k] = 0.0;}
      angle<<setw(3)<<(k+1)<<
	setw(30)<< kb[k] <<
	setw(15)<< theta[k] <<
	setw(10)<< kt1[k] <<
	//setw(10)<< kt2[k] <<
	setw(10)<< kt1[k]/3.0 <<
	setw(15)<< phi[k] << setw(15) << 0 <<endl;
    } 

  fin.close(); 

  return 0; 
}






