#include <zephyr/kernel.h>

#include <math.h>
#include "confusion.h"
#include "adc.h"
#include "keskipisteet.h"

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

int measurements[6][3]={
	                     {1,0,0},
						 {2,0,0},
						 {0,1,0},
						 {0,2,0},
						 {0,0,1},
						 {0,0,2}
};

int CM[6][6]= {0};



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
   /*******************************************
   Jos ja toivottavasti kun teet toteutuksen paloissa eli varmistat ensin,
   että etäisyyden laskenta 6 keskipisteeseen toimii ja osaat valita 6 etäisyydestä
   voittajaksi sen lyhyimmän etäisyyden, niin silloin voit käyttää tätä aliohjelmaa
   varmistaaksesi, että etäisuuden laskenta ja luokittelu toimii varmasti tunnetulla
   itse keksimälläsi sensoridatalla ja itse keksimilläsi keskipisteillä.
   *******************************************/
    
    int test_data[6][3] = {
        {1475, 1502, 1202}, // Suunta 0
        {1490, 1484, 1802}, // Suunta 1
        {1501, 1805, 1477}, // Suunta 2
        {1183, 1517, 1514}, // Suunta 3
        {1781, 1493, 1522}, // Suunta 4
        {1463, 1206, 1494}  // Suunta 5
    };
    
    for (int dir = 0; dir < 6; dir++) 
    {
        printk("\nSuunta %d \n", dir);
        
        for (int i = 0; i < 100; i++) 
        {
            // tämä lisää pientä "kohinaa" testidataan
            int x = test_data[dir][0] + (i % 61) - 30;
            int y = test_data[dir][1] + ((i*3) % 61) - 30;
            int z = test_data[dir][2] + ((i*7) % 61) - 30;
          
            int predicted = calculateDistanceToAllCentrePointsAndSelectWinner(x, y, z);
            
            CM[dir][predicted]++;
        }
        
        printk("Suunta %d done: 100 mittausta\n", dir);
    }
    
    printk("600 feikkimittausta tehty\n\n");
}


void makeOneClassificationAndUpdateConfusionMatrix(int direction)
{
   /**************************************
   Tee toteutus tälle ja voit tietysti muuttaa tämän aliohjelman sellaiseksi,
   että se tekee esim 100 kpl mittauksia tai sitten niin, että tätä funktiota
   kutsutaan 100 kertaa yhden mittauksen ja sen luokittelun tekemiseksi.
   ***************************************/

  struct Measurement m = readADCValue();
  printk("Mitattu arvo: x=%d, y=%d, z=%d (true dir=%d)\n", m.x, m.y, m.z, direction);

  int predicted = calculateDistanceToAllCentrePointsAndSelectWinner(m.x, m.y, m.z);

  CM[direction][predicted]++;

  printk("True=%d, Predicted=%d -- CM[%d][%d]++\n", direction, predicted, direction, predicted);

}

int calculateDistance(int x1, int y1, int z1, int x2, int y2, int z2)
{
   int dx = x1 - x2;
   int dy = y1 - y2;
   int dz = z1 - z2;
   return (dx*dx + dy*dy + dz*dz);
}

int calculateDistanceToAllCentrePointsAndSelectWinner(int x,int y,int z)
{
   /***************************************
   Tämän aliohjelma ottaa yhden kiihtyvyysanturin mittauksen x,y,z,
   laskee etäisyyden kaikkiin 6 K-means keskipisteisiin ja valitsee
   sen keskipisteen, jonka etäisyys mittaustulokseen on lyhyin.
   ***************************************/
      int winner = 0;
      int min_distance = 999999999; 
    
    for (int i = 0; i < 6; i++) 
    {
       
        int dx = x - CP[i][0];
        int dy = y - CP[i][1];
        int dz = z - CP[i][2];
        int dist = dx*dx + dy*dy + dz*dz;
        
        
        if (dist < min_distance) {
            min_distance = dist;
            winner = i;
        }
    }
    
    return winner;  // Palauta lähimmän keskipisteen indeksi (0-5)
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

