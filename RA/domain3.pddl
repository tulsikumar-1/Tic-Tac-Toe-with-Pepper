(define (domain tictactoe3)

    (:requirements
        :strips
        :typing
        :negative-preconditions
        :non-deterministic
    )
    
    (:types spot agent)
    
    (:constants
        TL TM TR
        ML MM MR
        BL BM BR - spot
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
            (and (when (and (not (marked TL x)) (not (marked TL o))) (marked TL o)))
            (and (when (and (not (marked TM x)) (not (marked TM o))) (marked TM o)))
            (and (when (and (not (marked TR x)) (not (marked TR o))) (marked TR o)))
            (and (when (and (not (marked ML x)) (not (marked ML o))) (marked ML o)))
            (and (when (and (not (marked MM x)) (not (marked MM o))) (marked MM o)))
            (and (when (and (not (marked MR x)) (not (marked MR o))) (marked MR o)))
            (and (when (and (not (marked BL x)) (not (marked BL o))) (marked BL o)))
            (and (when (and (not (marked BM x)) (not (marked BM o))) (marked BM o)))
            (and (when (and (not (marked BR x)) (not (marked BR o))) (marked BR o)))
      )
      )
    )

    
    
    (:action top_row
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked TL ?ag1)
            (marked TM ?ag1)
            (marked TR ?ag1)
            (not (win ?ag2))
            
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    (:action mid_row
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked ML ?ag1)
            (marked MM ?ag1)
            (marked MR ?ag1)
            (not (win ?ag2))
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    (:action bot_row
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked BL ?ag1)
            (marked BM ?ag1)
            (marked BR ?ag1)
            (not (win ?ag2))
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    (:action left_col
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked TL ?ag1)
            (marked ML ?ag1)
            (marked BL ?ag1)
            (not (win ?ag2))
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    (:action mid_col
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked TM ?ag1)
            (marked MM ?ag1)
            (marked BM ?ag1)
            (not (win ?ag2))
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    (:action right_col
        :parameters (?ag1 ?ag2 - agent)
        :precondition (and
            (actor ?ag1)
            (next ?ag1 ?ag2)
            (marked TR ?ag1)
            (marked MR ?ag1)
            (marked BR ?ag1)
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
            (marked TL ?ag1)
            (marked MM ?ag1)
            (marked BR ?ag1)
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
            (marked BL ?ag1)
            (marked MM ?ag1)
            (marked TR ?ag1)
            (not (win ?ag2))
        )
        :effect(and 
            (win ?ag1)
            (not (actor ?ag1))
            (actor ?ag2))
    )
    
    

)
