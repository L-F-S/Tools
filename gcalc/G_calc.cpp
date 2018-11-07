#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>
#include <time.h>
#include <stdbool.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/stat.h>

#define MAX_NBEADS (2000)

//#define DEBUG


void vec_prod (double *a, double *b, double *c);
double vec_dist (double *a, double *b);
void vec_sum (double *a, double *b, double *c);
void vec_diff (double *a, double *b, double *c);
double vec_dot (double *a, double *b);
void vec_scale (double *a, double k, double *c);
void vec_set (double *a, double *c);
double vec_norm (double *a);
void vec_normalize (double *a);
void vec_zero (double *a);
double compute_G(double *Seg1, int N_s1, double *Seg2, int N_s2, double dr);
FILE *fdbgL,*fdbg0,*fdbgT; //DBG
int step;



int main(int argc, char *argv[]) {
  

  clock_t begint = clock(); 
  FILE *input,*infile,*outfile;
  
  if(argc < 4){
    fprintf(stderr,"Error : 3 inputs  required:\n1)input vtf file\n2)input parameter file.\n3)output string\n");
    //fprintf(stderr,"Input example:\n\n#nsegment 1\n#nloop 2\n#start  0\n#end  -1\n#segment \n57\t47\n#loop\n99\t92\t116\n86\t92\t116\n");
    exit(1);
  }

  //open  input parameter file
  if((input = fopen(argv[2], "r")) == NULL) printf("\nError reading vtf file");


  //read parameters

  int N_parameters = 5;
  int parameter_check[N_parameters];

  char  **parameter;
  int ii;
  parameter = (char **) calloc(N_parameters, sizeof(char *));
  for(ii = 0; ii < N_parameters; ii++) { 
    parameter[ii] = (char *) calloc(1024, sizeof(char));
  }

  
  char string[1024];
  double value,width,dr;

  int nseg,nloo,start,end,i,slipseg;
  

  sprintf(parameter[0],"#start");        // starting frame (opt)
  sprintf(parameter[1],"#end");          // ending frame (opt)
  sprintf(parameter[2],"#dr");    // line integration step (opt)
  sprintf(parameter[3],"#closed1");    // is seg1 closed? (opt)
  sprintf(parameter[4],"#closed2");    // is seg2 closed? (opt)
  
  for(i = 0 ; i < N_parameters ; i++ ) parameter_check[i]=0; 
  int check,k,nonsort,closed1,closed2;
  k=0;
  closed1=0;
  closed2=0;
  //default values for optional parameters

  start=0;
  end=-1;
  dr=0.1;
  bzero(string, sizeof(string));
  while((check=fscanf(input,"%s %lf", string, &value))==2 && k<N_parameters) {
    for( i = 0 ; i < N_parameters ; i++ )
      {
	if ( strcmp( string, parameter[i] ) == 0 )
	  {
	    k++;
	    switch(i)
	      {
	      case 0:
		start = (int)value;
		parameter_check[i]=1;
		break;
	      case 1:
		end = (int)value;
		parameter_check[i]=1;
		break;
	      case 2:
		dr = (double)value;
		parameter_check[i]=1;
		break;
	      case 3:
		closed1 = 1;
		parameter_check[i]=1;
		break;
	      case 4:
		closed2 = 1;
		parameter_check[i]=1;
		break;
	      }
	  }
      }
    bzero(string, sizeof(string)); 
  }

  printf("c1 = %d \t c2 = %d\n",closed1,closed2);
  //lookup segment1 beads
  int l;
  rewind(input);
  l=0;
  do{
    fscanf ( input, "%s", string );
    l = strcmp ( string, "#segment1" );
    i++;
    if (i>1000)
      {
        fprintf(stderr,"Failed to find segment1 string in %s\n",argv[2]);
        fprintf(stderr,"Aborting.\n");
	exit(1);
      }
  }while( l !=0 );
  
  int s1i,s1f;
  fscanf(input, "%d %d\n", &s1i,&s1f);
  if(s1i>s1f){ //i bigger than f
    int temp=s1i-1;
    s1i=s1f-1;
    s1f=temp;
  }else{
    s1i=s1i-1;
    s1f=s1f-1;
  }

  //lookup segment2 beads
  rewind(input);
  l=0;
  do{
    fscanf ( input, "%s", string );
    l = strcmp ( string, "#segment2" );
    i++;
    if (i>1000)
      {
        fprintf(stderr,"Failed to find segment2 string in %s\n",argv[2]);
        fprintf(stderr,"Aborting.\n");
	exit(1);
      }
  }while( l !=0 );
  
  int s2i,s2f;
  fscanf(input, "%d %d\n", &s2i,&s2f);
  if(s2i>s2f){ //i bigger than f
    int temp=s2i-1;
    s2i=s2f-1;
    s2f=temp;
  }else{
    s2i=s2i-1;
    s2f=s2f-1;
  }
  
  



  int max_ind=s1f; 
  if(s2f>max_ind) max_ind=s2f; //largest index
  
  //allocate vector with all loop coordinates
  printf("segment 1 (internal): %d %d\n",s1i,s1f);
  int Nbeads1 = s1f-s1i+1;
  if(closed1){
    printf("segment 1 is closed from %d to %d\n",s1i,s1f);
    Nbeads1++; //add extra vector equal to first one
  }
  printf("segment 1 is %d beads long\n",Nbeads1);
  double  *s1xx;
  s1xx = (double *) calloc(3*Nbeads1, sizeof(double));
  
  
  //allocate vector with all coordinates
  printf("segment 2 (internal): %d %d\n",s2i,s2f);
  int Nbeads2=s2f-s2i+1;
  if(closed2){
    printf("segment 2 is closed from %d to %d\n",s2i,s2f);
    Nbeads2++; //add extra vector equal to first one
  }
  printf("segment 2 is %d beads long\n",Nbeads2);
  double  *s2xx;
  s2xx = (double *) calloc(3*Nbeads2, sizeof(double));

  //open  input traj file
  if((infile = fopen(argv[1], "r")) == NULL) printf("\nError reading vtf file");
  
  char line[1024];

  bzero(line, sizeof(line));
  bzero(string, sizeof(string));
  
  // 0- check if indexes make sense
  check=0;
  do{
    fgets(line,sizeof(line),infile); //get line
    sscanf (line, "%s", string); //get string
    check = strcmp ( string, "#Nbeads");
    if( feof(infile) ) {
      fprintf(stderr,"Error : Failed to find #Nbeads in the input file\n");
      exit(1);
    }
  }while( check !=0 );
  int Nbeads=0;
  sscanf (line, "%*s%d", &Nbeads); //get number of beads
  printf("Processing a %d beads trajectory, max_i = %d\n",Nbeads,max_ind);
  if(max_ind>Nbeads){
    fprintf(stderr,"Error : chosen indexes not available in the trajectory\n");
     exit(1);
  }

  //open output file
  char outname[1024];
  bzero(outname, sizeof(outname));
  sprintf(outname,"G_%s.dat",argv[3]);
  if((outfile = fopen(outname, "w")) == NULL) printf("\nError opening output file");

  step=0;
  int bottom=0;
    
  // 1- find starting point of trajectory
  check=0;
  do{
    bzero(string, sizeof(string));
    fgets(line,sizeof(line),infile); //get line
    sscanf (line, "%s", string); //get string
    check = strcmp ( string, "timestep");
    if( feof(infile) ) {
      fprintf(stderr,"Error : Failed to find coordinates in the input file\n");
      exit(1);
    }
  }while( check !=0 );

  //scan line for  the timestep
  sscanf (line, "%*s%*s%*s%*s%*s%*s%d",&step); //get step
  
  printf("first step %d\n",step);

  // 2- skip first frames

  while(step<start){
    check = 0;
    do{
      bzero(string, sizeof(string));
      fgets(line,sizeof(line),infile); //get line
      sscanf (line, "%s", string); //get string
      check = strcmp ( string, "timestep");
      if( feof(infile) ) {
	fprintf(stderr,"Error : Failed to find the starting frame in the input file\n");
	exit(1);
      }
    }while( check !=0 );
    
    //scan line for  the timestep
    sscanf (line, "%*s%*s%*s%*s%*s%*s%d",&step); //get step
    
  } //now step >= start, we can record the positions
  
  int read_frames = 0;
  printf("start recording at %d step\n",step);
  printf("%d\t%d\t%d\n",step,end,start);
  while((step <= end || end==-1 || start==end)){
    // record positions and go to next frame
    int s1beads=0;
    int s2beads=0;

    for(int k=0; k<=max_ind; k++){ //find i-th line
      fgets(line,sizeof(line),infile); //get line
      
      if(k>=s1i && k<=s1f){
	sscanf (line, "%lf%lf%lf", &s1xx[3*s1beads],&s1xx[3*s1beads+1],&s1xx[3*s1beads+2]); //get bead x
	s1beads++;
      }
      
      if(k>=s2i && k<=s2f){
	sscanf (line, "%lf%lf%lf", &s2xx[3*s2beads],&s2xx[3*s2beads+1],&s2xx[3*s2beads+2]); //get bead x
	s2beads++;
	//DBG
	//if(k==s2i || k==s2f){
	//  printf("%s",line);
	//  printf("%d %d\t%.4f\t%.4f\t%.4f\n",step,s2beads-1,s2xx[3*(s2beads-1)],s2xx[3*(s2beads-1)+1],s2xx[3*(sbeads-1)+2]);
	//}
      }
      
    }    
    if( feof(infile) ) {
      fprintf(stderr,"Error : trajectory unexpectedly interrupted.n");
      exit(1);
    }

    if(closed1){ //last position equal to first
      s1xx[3*(Nbeads1-1)]=s1xx[0];
      s1xx[3*(Nbeads1-1)+1]=s1xx[1];
      s1xx[3*(Nbeads1-1)+2]=s1xx[2];
    }
    
    if(closed2){ //last position equal to first
      s2xx[3*(Nbeads2-1)]=s2xx[0];
      s2xx[3*(Nbeads2-1)+1]=s2xx[1];
      s2xx[3*(Nbeads2-1)+2]=s2xx[2];
    }
    
    
    double G2=compute_G(s1xx, Nbeads1, s2xx, Nbeads2, dr);

    fprintf(outfile,"%d\t%.8f\n",step,G2);
        
    fflush(outfile);
    read_frames++;
    
    //find next frame
    check=0;
    bzero(string, sizeof(string));
    sscanf (line, "%s", string); //get string
    //if(step == 0 ) printf("%s\n",line);
    check = strcmp ( string, "timestep");
    
    while( check != 0){
      bzero(string, sizeof(string));
      fgets(line,sizeof(line),infile); //get line
      sscanf (line, "%s", string); //get string
      check = strcmp ( string, "timestep");
      if( feof(infile) ) {
	bottom=1;
	break;
      }
    }
    
    //scan line for  the timestep
    sscanf (line, "%*s%*s%*s%*s%*s%*s%d",&step); //get step
    
    //fgets(line,sizeof(line),infile); //next line
    if(bottom==1){
      printf( "end of file reached\n");
      break;
    }
  }
  
  printf("%d frames read\n",read_frames);
  
  fclose(input);
  fclose(infile);
  fclose(outfile);
  
  //free arrays
  
  free(s1xx);
  free(s2xx);

  

  
  for (ii = 0; ii < N_parameters; ii++) {
    free(parameter[ii]);
  }
  free(parameter);
  clock_t endt = clock();
  double time_spent = (double)(endt - begint) / CLOCKS_PER_SEC;
  printf("runtime = %.4f\n",time_spent);
  return(0); 
}

/*******************************/
void vec_diff (double *a, double *b, double *c)
{

  c[0] = b[0] - a[0];
  c[1] = b[1] - a[1];
  c[2] = b[2] - a[2];

}

/*******************************/
double vec_dist (double *a, double *b)
{

  int i;
  double dist=0;
  for (i =0; i < 3; i++)  dist+=(b[i]-a[i])*(b[i]-a[i]);
  dist=sqrt(dist);
  return(dist);
}

/*******************************/
void vec_sum (double *a, double *b, double *c)
{

  c[0] = a[0] + b[0];
  c[1] = a[1] + b[1];
  c[2] = a[2] + b[2];

}

/*******************************/
void vec_prod (double *a, double *b, double *c)
{

  c[0] = a[1] * b[2] - a[2] * b[1];
  c[1] = a[2] * b[0] - a[0] * b[2];
  c[2] = a[0] * b[1] - a[1] * b[0];
}
/*******************************/

void vec_scale (double *a, double k, double *c)
{
  int i;
  for (i = 0; i < 3; i++)
    {
      c[i] = k*a[i];
    }
}



double vec_dot (double *a, double *b)
{

  int i;
  double temp;

  temp = 0.0;
  for (i = 0; i < 3; i++)
    {
      temp += a[i] * b[i];
    }
  return (temp);
}

/*******************************/

double vec_norm (double *a)
{

  return (sqrt (vec_dot (a, a)));
}

/*******************************/
void vec_normalize (double *a)
{
  int i;
  double temp;

  temp = vec_norm (a);
  for (i = 0; i < 3; i++)
    {
      a[i] = a[i] / temp;
    }
}


void vec_zero (double *a)
{

  int i;
  for (i = 0; i < 3; i++)
    {
      a[i] = 0;
    }
}

void vec_set (double *a, double *c)
{

  int i;
  for (i = 0; i < 3; i++)
    {
      c[i] = a[i];
    }
}


bool vec_equal (double *a, double *b){
  int i;
  bool test(true) ;
  for (i = 0; i < 3; i++){
    if(a[i] != b[i]){
      test=false;
      break;
    }
  }
  return (test);
}




double compute_G(double *Seg1, int N_s1, double *Seg2, int N_s2, double dr){

  double G=0;
  double disti[3]={0};
  double distj[3]={0};
  double R_i[3]={0};
  double R_ik[3]={0};
  double R_j[3]={0};
  double R_jk[3]={0};
  double dR_i[3]={0};
  double dR_j[3]={0};
  double dR_i2[3]={0};
  double dR_j2[3]={0};
  double Rij[3]={0};
  double dxd[3]={0};

  
  
  double ndisti,dri,ndistj,drj,modRij,modRij3,Rijdxd;
  int ki,kj;
  
  //for over loop  segments
  for(int i=0; i<N_s1-1; i++){

    vec_diff(&Seg1[3*i],&Seg1[3*i+3],disti);  //dist i+1 and i

    //divide segment size by dr
    ndisti = vec_norm(disti);
    ki = nearbyint(ndisti/dr); // |loop[i+1]-loop[i]|/dr = ki.kd
    if(ki==0) ki=1; //if dr>dist dist=dr
    // exact dr
    dri = 1.0/ki; // dri = |loop[i+1]-loop[i]|/ki
    //DBG
    //fprintf(fdbgL,"%d  %d  %.8f  %.8f  %.8f\t\t%.8f  %.8f  %.8f\t\t%.8f  %.8f  %.8f\n",pbci1,ki,dri,ndisti,dri*ndisti,Seg1[3*i],Seg1[3*i+1],Seg1[3*i+2],Seg1[3*pbci1],Seg1[3*pbci1+1],Seg1[3*pbci1+2]);

    //fprintf(fdbg,"ls %d\t%d  %.10g\n",i,ki,dri); //DBG
    vec_scale(disti,dri,dR_i); // dR_i = dri*(loop[i+1]-loop[i])/|loop[i+1]-loop[i]| //this stays the same
    vec_scale(dR_i,0.5,dR_i2); 
    vec_sum(&Seg1[3*i],dR_i2,R_i);     // R_i = loop[i]+ (0.5)*dR_i // this is updated along loop[i+1]-loop[i]

    //loop on ki dr-chunks contributions
    //fprintf(fdbg,"%d  %.8f  %.8f  %.8f\t%.8f  %.8f  %.8f\t%.8f  %.8f  %.8f\n",i,loo[3*i],loo[3*i+1],loo[3*i+2],loo[3*(i+1)],loo[3*(i+1)+1],loo[3*(i+1)+2],dR_i[0],dR_i[1],dR_i[2]); //DBG
    for(int k=0; k<ki; k++){
      //fprintf(fdbg,"%d  %.8f  %.8f  %.8f\n",i,R_i[0],R_i[1],R_i[2]); //DBG
      //for over thread segments
      //fprintf(fdbgL,"%.8f\t%.8f\t%.8f\t%.8f\t%.8f\t%.8f\n",Seg1[3*i],Seg1[3*i+1],Seg1[3*i+2],R_i[0],R_i[1],R_i[2]); //DBG
      //fprintf(fdbg,"ls %d  ls_k %d\t%.4f  %.4f  %.4f\n",i,k,R_i[0],R_i[1],R_i[2]); //DBG
      for(int j=0; j<N_s2-1; j++){
	vec_diff(&Seg2[3*j],&Seg2[3*j+3],distj);  //dist j+1 and j
	//divide segment size by dr
	ndistj = vec_norm(distj);
	kj = nearbyint(ndistj/dr); // |thread[j+1]-thread[j]|/dr = ki.kd
	if(kj==0) kj=1; //if dr>dist dist=dr
	// exact dr
	drj = 1.0/kj; // drj = |thread[j+1]-thread[j]|/kj
	vec_scale(distj,drj,dR_j); // dR_j = drj*(thread[j+1]-thread[j])/|thread[j+1]-thread[j]| //this stays the same
	vec_scale(dR_j,0.5,dR_j2);  
	vec_sum(&Seg2[3*j],dR_j2,R_j);     // R_j = thread[j]+ (0.5)*dR_j // this is updated along thread[j+1]-thread[j]
	
	//loop on ki dr-chunks contributions 
	for(int m=0; m<kj; m++){
	  //fprintf(fdbgT,"%.8f\t%.8f\t%.8f\t%.8f\t%.8f\t%.8f\n",Seg2[3*j],Seg2[3*j+1],Seg2[3*j+2],R_j[0],R_j[1],R_j[2]); //DBG
	  //fprintf(fdbg,"ts %d  ts_k %d\t%.4f  %.4f  %.4f\n",j,m,R_j[0],R_j[1],R_j[2]); //DBG
	  //increment G
	  vec_diff(R_i,R_j,Rij);  //dist i j
	  modRij = vec_norm(Rij); //magnitude
	  modRij3 = modRij*modRij*modRij;

	  vec_prod(dR_i,dR_j,dxd);   // cross product
	  Rijdxd = vec_dot(Rij,dxd);

	  G+=Rijdxd/modRij3;
	  
	  vec_sum(R_j,dR_j,R_jk);// R_jk = R_j + dR_j*kj // R_j updated along thread[j+1]-thread[j]
	  vec_set(R_jk,R_j); //update R_i
	}
      }

      vec_sum(R_i,dR_i,R_ik);// R_ik = R_i + dR_i*ki // R_i updated along loop[i+1]-loop[i]
      vec_set(R_ik,R_i); //update R_i
    }
  }	
  G=G/(4*M_PI);
  return(G);
}

  
