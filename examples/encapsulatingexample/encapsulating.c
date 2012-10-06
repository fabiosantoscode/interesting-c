
/* capsule Counter (of int) */
/*! Array_data is declared outside this scope*/
Array_data Counter_all_counters;
typedef struct Counter_data{
    int super;
    
}s_Counter;

Counter_data Counter_constructor(Counter_data this){
    this.super = 0;
    Array_add(Counter_all_counters, (void*)&this);
    return this;
}

int Counter_property_get_this(Counter_data this){
    return this.super + 1;
}

void Counter_increment(Counter_data this){
    this.super++;
}


/* capsule LinkedListNode<type ArrayItemType> */
typedef struct LinkedListNode_data{
    void *data;
    struct LinkedListNode_data *next;
}LinkedListNode_data;

LinkedListNode_data LinkedListNode_constructor(LinkedListNode_data this, void *data){
    this.data = data;
    this.next_node = null;
}


/* capsule LinkedList<type T> (of pointer to hidden LinkedListNode<T>) */
typedef struct LinkedList_data{
    LinkedListNode_data *super;
    int size;
}LinkedList_data;

void LinkedList_push(LinkedList_data this, void* data){
    LinkedListNode_data *new_node = 
        (LinkedListNode_data*)malloc(sizeof(LinkedListNode_data);
    LinkedListNode_constructor(*new_node, data);
    
    if (this.super == null){
        this.size = 1;
        this.super = new_node;
        return;
    }
    
    new_node->next_node = 
}
