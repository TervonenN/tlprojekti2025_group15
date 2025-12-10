#include <zephyr/kernel.h>
#include <math.h>
#include "confusion.h"
#include "adc.h"
#include "centroids.h"

/* 
  K-means algorithm should provide 6 center points with
  3 values x,y,z. Let's test measurement system with known
  center points. I.e. x,y,z are supposed to have only values
  1 = down and 2 = up
  
  CP matrix is thus the 6 center points got from K-means algoritm
  teaching process. This should actually come from include file like
  #include "KmeansCenterPoints.h"
  
  And measurements matrix is just fake matrix for testing purpose
  actual measurements are taken from ADC when accelerator is connected.
*/ 

/*
int CP[6][3]={
	                     {1,0,0},
						 {2,0,0},
						 {0,1,0},
						 {0,2,0},
						 {0,0,1},
						 {0,0,2}
};
*/

int measurements[6][3]={
	                     {1,0,0},
						 {2,0,0},
						 {0,1,0},
						 {0,2,0},
						 {0,0,1},
						 {0,0,2}
};

int CM[6][6]= {0};

int clusterToClass[6] = {0, 3, 5, 4, 2, 1}; 


void printConfusionMatrix(void)
{
	printk("Confusion matrix = \n");
	printk("   cp1 cp2 cp3 cp4 cp5 cp6\n");
	for(int i = 0;i<6;i++)
	{
		printk("cp%d %d   %d   %d   %d   %d   %d\n",i+1,CM[i][0],CM[i][1],CM[i][2],CM[i][3],CM[i][4],CM[i][5]);
	}
}

void makeHundredFakeClassifications(void)
{
   printk("testi 1\n");

   float testidata [6][3]={
      {1500,1500,1200},
      {1200,1500,1500},
      {1500,1200,1500},
      {1800,1500,1500},
      {1500,1800,1500},
      {1500,1500,1800}
   };

   for(int a = 0; a<6; a++)
   {
      float x = testidata[a][0];
      float y = testidata[a][1];
      float z = testidata[a][2];

      for(int i = 0; i<100; i++)
      {
         int b = calculateDistanceToAllCentrePointsAndSelectWinner(x,y,z);
         CM[a][b]++;
      }
   }
   
   
   printk("Make your own implementation for this function if you need this\n");
}

void makeOneClassificationAndUpdateConfusionMatrix(int *direction)
{
   /**************************************
   Tee toteutus tälle ja voit tietysti muuttaa tämän aliohjelman sellaiseksi,
   että se tekee esim 100 kpl mittauksia tai sitten niin, että tätä funktiota
   kutsutaan 100 kertaa yhden mittauksen ja sen luokittelun tekemiseksi.
   **************************************/

  struct Measurement m = readADCValue();
  printk("Mitattu arvo: x=%d, y=%d, z=%d (true dir=%d)\n", m.x, m.y, m.z, *direction);

  int predicted = calculateDistanceToAllCentrePointsAndSelectWinner(m.x, m.y, m.z);

  CM[*direction][predicted]++;
  
    if (predicted!=*direction){
   *direction=predicted;
   printk("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n");
   }

  printk("True=%d, Predicted=%d -- CM[%d][%d]++\n", *direction, predicted, *direction, predicted );
   
 

}

int calculateDistanceToAllCentrePointsAndSelectWinner(int x,int y,int z)
{
   /***************************************
   Tämän aliohjelma ottaa yhden kiihtyvyysanturin mittauksen x,y,z,
   laskee etäisyyden kaikkiin 6 K-means keskipisteisiin ja valitsee
   sen keskipisteen, jonka etäisyys mittaustulokseen on lyhyin.
   ***************************************/
   //printk("\nTESTI 2\n\n");

   float maxEtaisyys = 100000.0f; // numpyssä käytin maximiraja-arvoa inf tilalta.
   int parasTulos = 0;
   

   for (int i = 0; i<6; i++)
   {
      float dx = CENTROIDS[i][0] -x;
      float dy = CENTROIDS[i][1] -y;
      float dz = CENTROIDS[i][2] -z;

      float etaisyys = dx*dx + dy*dy + dz*dz;

      if (etaisyys < maxEtaisyys){
         maxEtaisyys = etaisyys;
         parasTulos = i;
      }
   }


   return parasTulos;
  

   printk("Make your own implementation for this function if you need this\n");
   //return 0;
}

void resetConfusionMatrix(void)
{
	for(int i=0;i<6;i++)
	{ 
		for(int j = 0;j<6;j++)
		{
			CM[i][j]=0;
		}
	}
}

