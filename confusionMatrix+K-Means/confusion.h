#ifndef CONFUSION_MATRIX_H
#define CONFUSION_MATRIX_H


void printConfusionMatrix(void);
void makeHundredFakeClassifications(void);
void makeOneClassificationAndUpdateConfusionMatrix(int *direction);
int calculateDistanceToAllCentrePointsAndSelectWinner(int,int,int);
void resetConfusionMatrix(void);


#endif
