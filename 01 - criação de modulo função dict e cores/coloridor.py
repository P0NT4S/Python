def colorir(txt, estilo, cor, fundo):

    GERAL = "\033["
    TIPO = {"vanilla" : "0", 
            "bold" : "1", 
            "sub" : "4", 
            "invert" : "7"}
    
    COLOR = {"white" : "30", 
           "red" : "31", 
           "green" : "32", 
           "yellow" : "33", 
           "blue" : "34", 
           "purple" : "35", 
           "cyan" : "36",
           "gray" : "37"}
    
    BACK = {"none" : "",
            "white" : "40", 
            "red" : "41", 
            "green" : "42", 
            "yellow" : "43", 
            "blue" : "44", 
            "purple" : "45", 
            "cyan" : "46",
            "gray" : "47"}

    return f"{GERAL}{TIPO[estilo]};{COLOR[cor]};{BACK[fundo]}m{txt}{GERAL}m"


