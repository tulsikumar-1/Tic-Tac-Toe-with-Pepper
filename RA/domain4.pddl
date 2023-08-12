(define (domain tictactoe4)

    (:requirements
        :strips
        :typing
        :negative-preconditions
        :non-deterministic
    )
    
    (:types spot agent)
    
    (:constants
        A1 A2 A3 A4
        B1 B2 B3 B4
        C1 C2 C3 C4
        D1 D2 D3 D4 - spot
        x o  EMPTY - agent
    )
    
    (:predicates
        (actor ?ag - agent)
        (next ?ag1 - agent ?ag2 - agent)
        (marked ?loc - spot ?ag - agent)
        (win ?ag - agent)
    )




    (:action robot
        :parameters (?loc - spot)
        :precondition (and
            (actor x)
            (next x o)
            (not (marked ?loc x))
            (not (marked ?loc o))
            
        )
        :effect (and
            (marked ?loc x)
            (not (actor x))
            (actor o)
            (next o x)
        )
    )
    
    (:action human
    :parameters (?loc - spot)
    :precondition (and
        (actor o)
        (next o x)
        (not (marked ?loc x))
        (not (marked ?loc o))
       
    )
    :effect 
      ( and 
      (not (actor o)) (actor x) (next x o)
      (oneof
            (and (when (and (not (marked A1 x)) (not (marked A1 o))) (marked A1 o)))
            (and (when (and (not (marked A2 x)) (not (marked A2 o))) (marked A2 o)))
            (and (when (and (not (marked A3 x)) (not (marked A3 o))) (marked A3 o)))
            (and (when (and (not (marked A4 x)) (not (marked A4 o))) (marked A4 o)))
            (and (when (and (not (marked B1 x)) (not (marked B1 o))) (marked B1 o)))
            (and (when (and (not (marked B2 x)) (not (marked B2 o))) (marked B2 o)))
            (and (when (and (not (marked B3 x)) (not (marked B3 o))) (marked B3 o)))
            (and (when (and (not (marked B4 x)) (not (marked B4 o))) (marked B4 o)))
            (and (when (and (not (marked C1 x)) (not (marked C1 o))) (marked C1 o)))
            (and (when (and (not (marked C2 x)) (not (marked C2 o))) (marked C2 o)))
            (and (when (and (not (marked C3 x)) (not (marked C3 o))) (marked C3 o)))
            (and (when (and (not (marked C4 x)) (not (marked C4 o))) (marked C4 o)))
            (and (when (and (not (marked D1 x)) (not (marked D1 o))) (marked D1 o)))
            (and (when (and (not (marked D2 x)) (not (marked D2 o))) (marked D2 o)))
            (and (when (and (not (marked D3 x)) (not (marked D3 o))) (marked D3 o)))
            (and (when (and (not (marked D4 x)) (not (marked D4 o))) (marked D4 o)))
      )
      )
    )

    
    
    (:action A_row
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked A1 ?ag1)
            (marked A2 ?ag1)
            (marked A3 ?ag1)
            (marked A4 ?ag1)            
            (not (win ?ag2))
            
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    (:action B_row
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked B1 ?ag1)
            (marked B2 ?ag1)
            (marked B3 ?ag1)
            (marked B4 ?ag1)            
            (not (win ?ag2))
            
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    (:action C_row
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked C1 ?ag1)
            (marked C2 ?ag1)
            (marked C3 ?ag1)
            (marked C4 ?ag1)            
            (not (win ?ag2))
            
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    
    (:action D_row
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked D1 ?ag1)
            (marked D2 ?ag1)
            (marked D3 ?ag1)
            (marked D4 ?ag1)            
            (not (win ?ag2))
            
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )    
    
    
    (:action A1_col
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked A1 ?ag1)
            (marked B1 ?ag1)
            (marked C1 ?ag1)
            (marked D1 ?ag1)
            (not (win ?ag2))
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    (:action A2_col
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked A2 ?ag1)
            (marked B2 ?ag1)
            (marked C2 ?ag1)
            (marked D2 ?ag1)
            (not (win ?ag2))
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    (:action A3_col
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked A3 ?ag1)
            (marked B3 ?ag1)
            (marked C3 ?ag1)
            (marked D3 ?ag1)
            (not (win ?ag2))
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    (:action A4_col
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked A4 ?ag1)
            (marked B4 ?ag1)
            (marked C4 ?ag1)
            (marked D4 ?ag1)
            (not (win ?ag2))
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    (:action down_diag
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked A1 ?ag1)
            (marked B2 ?ag1)
            (marked C3 ?ag1)
            (marked D3 ?ag1)
            (not (win ?ag2))
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    (:action up_diag
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked A4 ?ag1)
            (marked B3 ?ag1)
            (marked C2 ?ag1)
            (marked D1 ?ag1)
            (not (win ?ag2))
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    

)
