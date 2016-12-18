#include "linear_sequence_assoc.h"

typedef struct _node {
    LSQ_IntegerIndexT key;
    LSQ_BaseTypeT value;
    unsigned char height;
    struct _node* left;
    struct _node* right;
    struct _node* parent;
} NodeT;

typedef struct {
    NodeT* root;
    unsigned int size;
} AVL_TreeT;

typedef enum {
    IS_BEFORE_FIRST,
    IS_DEREFERENCABLE,
    IS_PAST_REAR
} IteratorStateT;

typedef struct {
    AVL_TreeT* tree;
    NodeT* node;
    IteratorStateT state;
} IteratorT;

static IteratorT* CreateIterator(AVL_TreeT* Tree, NodeT* Node, IteratorStateT State) {
    IteratorT* i = malloc(sizeof(IteratorT));
    if (i == NULL) {
        return NULL;
    }
    i->tree = Tree;
    i->node = Node;
    i->state = State;
    return i;
}

static void DestroyNode(NodeT* Node) {
    if (Node) {
        DestroyNode(Node->left);
        DestroyNode(Node->right);
        free(Node);
    }
}

static NodeT* CreateNode(LSQ_IntegerIndexT Key, LSQ_BaseTypeT Value) {
    NodeT* t = malloc(sizeof(NodeT));
    if (t == NULL) {
        return NULL;
    }
    t->key = Key;
    t->value = Value;
    t->left = NULL;
    t->right = NULL;
    t->parent = NULL;
    t->height = 1;
    return t;
}

static inline unsigned char Height(NodeT* Node) {
    return Node != NULL ? Node->height : 0;
}

static inline int BalanceFactor(NodeT* Node) {
    return Height(Node->left) - Height(Node->right);
}

static void FixHeight(NodeT* Node) {
    unsigned char hl = Height(Node->left);
    unsigned char hr = Height(Node->right);
    Node->height = (unsigned char)((hl > hr ? hl : hr) + 1);
}

static void ReplaceNode(AVL_TreeT* Tree, NodeT* Node, NodeT* NewNode) {
    if (NewNode != NULL)
        NewNode->parent = Node->parent;
    if (Node->parent == NULL)
        Tree->root = NewNode;
    else {
        if (Node->parent->left == Node)
            Node->parent->left = NewNode;
        else
            Node->parent->right = NewNode;
    }
}

static void RotateRight(AVL_TreeT* Tree, NodeT* Node) {
    NodeT* new_root = Node->left;
    ReplaceNode(Tree, Node, new_root);
    Node->left = new_root->right;
    if (Node->left)
        Node->left->parent = Node;
    Node->parent = new_root;
    new_root->right = Node;
    FixHeight(Node);
    FixHeight(new_root);
}

static void RotateLeft(AVL_TreeT* Tree, NodeT* Node) {
    NodeT* new_root = Node->right;
    ReplaceNode(Tree, Node, new_root);
    Node->right = new_root->left;
    if (Node->right)
        Node->right->parent = Node;
    Node->parent = new_root;
    new_root->left = Node;
    FixHeight(Node);
    FixHeight(new_root);
}

static void Balance(AVL_TreeT* Tree, NodeT* Node, unsigned char StopBalance) {
    NodeT* parent;
    unsigned char balance;
    while (Node != NULL) {
        FixHeight(Node);
        balance = BalanceFactor(Node);
        parent = Node->parent;
        if (abs(balance) == StopBalance)
            return;
        if (balance == -2) {
            if (BalanceFactor(Node->right) > 0)
                RotateRight(Tree, Node->right);
            RotateLeft(Tree, Node);
        }
        else if (balance == 2) {
            if (BalanceFactor(Node->left) < 0)
                RotateLeft(Tree, Node->left);
            RotateRight(Tree, Node);
        }
        Node = parent;
    }
}

static NodeT* FindMin(NodeT* Node) {
    while (Node->left != NULL)
        Node = Node->left;
    return Node;
}

static NodeT* FindMax(NodeT* Node) {
    while (Node->right != NULL)
        Node = Node->right;
    return Node;
}

static NodeT* Find(NodeT* Node, LSQ_IntegerIndexT Key) {
    while (Node != NULL && Node->key != Key) {
        if (Node->key < Key)
            Node = Node->right;
        else
            Node = Node->left;
    }
    return Node;
}

LSQ_HandleT LSQ_CreateSequence(void) {
    AVL_TreeT* t = malloc(sizeof(AVL_TreeT));
    if (t == NULL) {
        return LSQ_HandleInvalid;
    }
    t->size = 0;
    t->root = NULL;
    return t;
}

void LSQ_DestroySequence(LSQ_HandleT handle) {
    if (handle == LSQ_HandleInvalid) {
        return;
    }
    DestroyNode(((AVL_TreeT*)handle)->root);
    free(handle);
}

LSQ_IntegerIndexT LSQ_GetSize(LSQ_HandleT handle) {
    return handle == LSQ_HandleInvalid ? 0 : ((AVL_TreeT*)handle)->size;
}

int LSQ_IsIteratorDereferencable(LSQ_IteratorT iterator) {
    return iterator != LSQ_HandleInvalid && ((IteratorT*)iterator)->state == IS_DEREFERENCABLE;
}

int LSQ_IsIteratorPastRear(LSQ_IteratorT iterator) {
    return iterator != LSQ_HandleInvalid && ((IteratorT*)iterator)->state == IS_PAST_REAR;
}

int LSQ_IsIteratorBeforeFirst(LSQ_IteratorT iterator) {
    return iterator != LSQ_HandleInvalid && ((IteratorT*)iterator)->state == IS_BEFORE_FIRST;
}

LSQ_BaseTypeT* LSQ_DereferenceIterator(LSQ_IteratorT iterator) {
    if (iterator == LSQ_HandleInvalid || ((IteratorT*)iterator)->state != IS_DEREFERENCABLE) {
        return LSQ_HandleInvalid;
    }
    return &(((IteratorT*)iterator)->node->value);
}

LSQ_IntegerIndexT LSQ_GetIteratorKey(LSQ_IteratorT iterator) {
    if (iterator == LSQ_HandleInvalid || ((IteratorT*)iterator)->state != IS_DEREFERENCABLE) {
        return -1;
    }
    return ((IteratorT*)iterator)->node->key;
}

LSQ_IteratorT LSQ_GetElementByIndex(LSQ_HandleT handle, LSQ_IntegerIndexT index) {
    if (handle == LSQ_HandleInvalid) {
        return LSQ_HandleInvalid;
    }
    NodeT* n = Find(((AVL_TreeT*)handle)->root, index);
    return CreateIterator((AVL_TreeT*)handle, n, n != NULL ? IS_DEREFERENCABLE : IS_PAST_REAR);
}

LSQ_IteratorT LSQ_GetFrontElement(LSQ_HandleT handle) {
    if (handle == LSQ_HandleInvalid) {
        return LSQ_HandleInvalid;
    }
    IteratorT* it = CreateIterator((AVL_TreeT *)handle, NULL, IS_BEFORE_FIRST);
    if (!it) {
        return LSQ_HandleInvalid;
    }
    LSQ_AdvanceOneElement(it);
    return it;
}

LSQ_IteratorT LSQ_GetPastRearElement(LSQ_HandleT handle) {
    if (handle == LSQ_HandleInvalid) {
        return LSQ_HandleInvalid;
    }
    return CreateIterator((AVL_TreeT *)handle, NULL, IS_PAST_REAR);
}

void LSQ_DestroyIterator(LSQ_IteratorT iterator) {
    if (iterator == LSQ_HandleInvalid) {
        return;
    }
    free(iterator);
}

void LSQ_AdvanceOneElement(LSQ_IteratorT iterator) {
    NodeT* node = NULL;
    NodeT* parent = NULL;
    if (iterator == LSQ_HandleInvalid || ((IteratorT*)iterator)->state == IS_PAST_REAR)
        return;
    if (((IteratorT*)iterator)->state == IS_BEFORE_FIRST) {
        if (((IteratorT*)iterator)->tree->root == NULL)
            ((IteratorT*)iterator)->state = IS_PAST_REAR;
        else {
            ((IteratorT*)iterator)->node = FindMin(((IteratorT*)iterator)->tree->root);
            ((IteratorT*)iterator)->state = IS_DEREFERENCABLE;
        }
        return;
    }
    node = ((IteratorT*)iterator)->node;
    while (node->parent != NULL && node->right == parent) {
        parent = node;
        node = node->parent;
    }
    if (node->right == parent) {
        ((IteratorT*)iterator)->state = IS_PAST_REAR;
        ((IteratorT*)iterator)->node = NULL;
    }
    else {
        if (node != ((IteratorT*)iterator)->node)
            ((IteratorT*)iterator)->node = node;
        else
            if (node->right)
                ((IteratorT*)iterator)->node = FindMin(node->right);
    }
}

void LSQ_RewindOneElement(LSQ_IteratorT iterator) {
    NodeT* node = NULL;
    NodeT* parent = NULL;
    if (iterator == LSQ_HandleInvalid || ((IteratorT*)iterator)->state == IS_BEFORE_FIRST)
        return;
    if (((IteratorT*)iterator)->state == IS_PAST_REAR) {
        if (((IteratorT*)iterator)->tree->root == NULL)
            ((IteratorT*)iterator)->state = IS_BEFORE_FIRST;
        else {
            ((IteratorT*)iterator)->node = FindMax(((IteratorT*)iterator)->tree->root);
            ((IteratorT*)iterator)->state = IS_DEREFERENCABLE;
        }
        return;
    }
    node = ((IteratorT*)iterator)->node;
    while (node->parent != NULL && node->left == parent) {
        parent = node;
        node = node->parent;
    }
    if (node->left == parent) {
        ((IteratorT*)iterator)->state = IS_BEFORE_FIRST;
        ((IteratorT*)iterator)->node = NULL;
    }
    else {
        if (node != ((IteratorT*)iterator)->node)
            ((IteratorT*)iterator)->node = node;
        else
            if (node->left)
                ((IteratorT*)iterator)->node = FindMax(node->left);
    }
}

void LSQ_ShiftPosition(LSQ_IteratorT iterator, LSQ_IntegerIndexT shift) {
    if (iterator == LSQ_HandleInvalid) {
        return;
    }
    while (shift > 0) {
        LSQ_AdvanceOneElement(iterator);
        --shift;
    }
    while (shift < 0) {
        LSQ_RewindOneElement(iterator);
        ++shift;
    }
}

void LSQ_SetPosition(LSQ_IteratorT iterator, LSQ_IntegerIndexT pos) {
    if (iterator == LSQ_HandleInvalid) {
        return;
    }
    ((IteratorT*)iterator)->state = IS_BEFORE_FIRST;
    LSQ_ShiftPosition(iterator, pos + 1);
}

void LSQ_InsertElement(LSQ_HandleT handle, LSQ_IntegerIndexT key, LSQ_BaseTypeT value) {
    if (handle == LSQ_HandleInvalid) {
        return;
    }
    NodeT* node = NULL;
    NodeT* parent = NULL;
    if (((AVL_TreeT*)handle)->root == NULL) {
        ((AVL_TreeT*)handle)->root = CreateNode(key, value);
        if (((AVL_TreeT*)handle) == NULL)
            return;
        ((AVL_TreeT*)handle)->root->parent = NULL;
        ((AVL_TreeT*)handle)->size++;
        return;
    }
    parent = ((AVL_TreeT*)handle)->root;
    for (;;) {
        if (key < parent->key) {
            if (parent->left == NULL)
                break;
            parent = parent->left;
        }
        else {
            if (key > parent->key) {
                if (parent->right == NULL)
                    break;
                parent = parent->right;
            }
            else {
                parent->value = value;
                return;
            }
        }
    }
    node = CreateNode(key, value);
    node->parent = parent;
    if (node == NULL) {
        return;
    }
    ((AVL_TreeT*)handle)->size++;
    if (key < parent->key)
        parent->left = node;
    else
        parent->right = node;
    Balance(((AVL_TreeT*)handle), parent, 0);
}

void LSQ_DeleteFrontElement(LSQ_HandleT handle) {
    LSQ_IteratorT it = LSQ_GetFrontElement(handle);
    if (handle == LSQ_HandleInvalid || it == LSQ_HandleInvalid) {
        return;
    }
    LSQ_DeleteElement(handle, LSQ_GetIteratorKey(it));
    LSQ_DestroyIterator(it);
}

void LSQ_DeleteRearElement(LSQ_HandleT handle) {
    LSQ_IteratorT it = LSQ_GetFrontElement(handle);
    if (handle == LSQ_HandleInvalid || it == LSQ_HandleInvalid) {
        return;
    }
    LSQ_RewindOneElement(it);
    LSQ_DeleteElement(handle, LSQ_GetIteratorKey(it));
    LSQ_DestroyIterator(it);
}

void LSQ_DeleteElement(LSQ_HandleT handle, LSQ_IntegerIndexT key) {
    if (handle == LSQ_HandleInvalid || LSQ_GetSize(handle) == 0) {
        return;
    }
    NodeT* node = NULL;
    NodeT* parent = NULL;
    node = Find(((AVL_TreeT*)handle)->root, key);
    if (node == NULL)
        return;
    parent = node->parent;
    if (node->left == NULL && node->right == NULL)
        ReplaceNode(((AVL_TreeT*)handle), node, NULL);
    else {
        if (node->left && node->right) {
            NodeT* left = FindMin(node->right);
            int new_key = left->key;
            node->value = left->value;
            LSQ_DeleteElement(handle, left->key);
            node->key = new_key;
            return;
        }
        else
            if (node->left != NULL)
                ReplaceNode(((AVL_TreeT*)handle), node, node->left);
            else
                ReplaceNode(((AVL_TreeT*)handle), node, node->right);
    }
    free(node);
    ((AVL_TreeT*)handle)->size--;
    Balance(((AVL_TreeT*)handle), parent, 1);
}