#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
struct experimentData{
    float krw0__ ; //ajustavel
    float krg0__ ; // ajustavel
    float lamb__ ; // ajustavel
    float swc__ ; // ajustavel
    float sw__ ; // vai variar na conta, mas é o valor inicial da saturação
    float sg__ ; // constante, sg é o resultado do sw-swc se me lembro bem (saturação de liquido - saturação conata = saturação do gas) já q sgr pode ser considerado 0
    float mrf__ ; // valor referente ao sufactante 
    float phi__ ; // valor da porosidade
    float volW__ ; // volume de agua dentro do experimento (resultado da massaFinal - massaInicial do experimento)
    float volt__ ; // volume total do ambiente
    float muw; // valor fixo
    float mug; // valor fixo
        //Condicao inicial
    float Sw_0 ; //fixo 
        //Condicao de Contorno
    float sw_a ;//gas  e espuma
};

struct ambientData{
    float h_x; //step de deslocamento em x
    float h_y; //step de deslocamento em y
    float h_t; //step de tempo em segundos
    float xT ; //espaço total de deslocamento em x
    float yT ; //espaço total de deslocamento em y
    float timeT ; //tempo total para o deslocamento

    float *x;     
    float *y;
    float *t;

    float tam ; //dimensão do sistema
    float steps ; //numero de passos de tempo
    float *sol_tempo ; // primeira fase (agua)
    float *sol_tempo2 ;// segunda fase (ar ou espuma)

    float *Sw;
    float *Sg;
    
    float *Sw_new;
};


float fw_(sw,sg, mrf,krw0, krg0,lamb, swc){
    float lambw = lambw_(sw,krw0,lamb,swc);
    float lambt = lambw_(sw,krw0,lamb,swc)+lambg_(sg,mrf,krg0,lamb,swc,sw);
    return lambw/lambt;
}

float swe_(sw,swc,sgr){

    return (sw - swc)/(1-swc-sgr);

};

float lambw_(sw,krw0,lamb,swc){
    float muw = 0 ;// fixo
    float krw = krw_(sw,krw0,lamb,swc);
    return (krw*sw)/muw;
}
   

float lambg_(sg,mrf,krg0,lamb,swc,sw){
    float mug = 0; // fixo
    float krg = krg_(krg0,lamb,swc,sw);
    return (krg*sg)/(mug*mrf);
}
float krw_(sw,krw0,lamb,swc){
    float sgr = 0; // fixo 
    float swe = swe_(sw,swc,sgr);
    return krw0*(pow(swe,lamb));
}

float krg_(krg0,lamb,swc,sw){
    float sgr = 0; // fixo 
    float swe = swe_(sw,swc,sgr);
    return krg0*(1-pow(swe,(3-(2/lamb))));
}
float phi_(volW,volT){
    return volW/volT;
}
  


int main(int argc, char const *argv[])

{
    /* code */
    printf("ola mundo");
    return 0;
}
