
void do_something(int number, char* str, float f){
    //...
}

int main(){
    // usable with any iterable
    int int1=0;
    char *str1="";
    float float1=14.1f;
    void *function_arguments[3] = {&int1, str1, &float1};
    do_something((int)*function_arguments[0], (char*)*function_arguments[1], (float)*function_arguments[2]);
    
    function_arguments[0] = 1;
    function_arguments[1] = "";
    function_arguments[2] = 14.1;
    do_something(*function_arguments[0], *function_arguments[1], *function_arguments[2]);
    
    return 0;
}

