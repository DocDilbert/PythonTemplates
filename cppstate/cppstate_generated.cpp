
enum StateId
{
  ID_STATEA
  ID_STATEB
  ID_STATEC
  ID_STATED
}

class IStateMachine
{
  public:
  	virtual void setNextState(StateId state) = 0;
}


class IState 
{
  public:

    /// This method returns the Id of the state
    virtual StateId update getId() = 0;

    /// The entry method is called by statemachine the first time this
    /// state is executed
    virtual void entry() = 0;

    /// The update method is called every time when the state is 
    /// active
    virtual void update() = 0;
}

class StateA : public IState
{
public:
    StateA::StateA() 
    {
    }
    
    StateId getId()
    {
        return ID_STATEA;
    }
    
    BOOL checkTransitionFromAtoB()
    {
        // If transition must be executed return true.
        return false;
    }
    
    BOOL checkTransitionFromAtoD()
    {
        // If transition must be executed return true.
        return false;
    }
    
    void processTransitions()
    {
        if (checkTransitionFromAtoB())
        {
            setNextState(StateB);
            return;
        }
        
        if (checkTransitionFromAtoD())
        {
            setNextState(StateD);
            return;
        }
    }
    
    void entry()
    {
    }
    
    void update()
    {
        processTransitions();
        
        // Insert state code here
    }
    
private:
    void setNextState(StateId state)
    {
        stateMachine.setNextState(state);
    }
    
    IStateMachine& stateMachine;
}

class StateB : public IState
{
public:
    StateB::StateB() 
    {
    }
    
    StateId getId()
    {
        return ID_STATEB;
    }
    
    void processTransitions()
    {
        // Check for transitions here ...
    }
    
    void entry()
    {
    }
    
    void update()
    {
        processTransitions();
        
        // Insert state code here
    }
    
private:
    void setNextState(StateId state)
    {
        stateMachine.setNextState(state);
    }
    
    IStateMachine& stateMachine;
}

class StateC : public IState
{
public:
    StateC::StateC() 
    {
    }
    
    StateId getId()
    {
        return ID_STATEC;
    }
    
    BOOL checkTransitionFromCtoA()
    {
        // If transition must be executed return true.
        return false;
    }
    
    void processTransitions()
    {
        if (checkTransitionFromCtoA())
        {
            setNextState(StateA);
            return;
        }
    }
    
    void entry()
    {
    }
    
    void update()
    {
        processTransitions();
        
        // Insert state code here
    }
    
private:
    void setNextState(StateId state)
    {
        stateMachine.setNextState(state);
    }
    
    IStateMachine& stateMachine;
}

class StateD : public IState
{
public:
    StateD::StateD() 
    {
    }
    
    StateId getId()
    {
        return ID_STATED;
    }
    
    void processTransitions()
    {
        // Check for transitions here ...
    }
    
    void entry()
    {
    }
    
    void update()
    {
        processTransitions();
        
        // Insert state code here
    }
    
private:
    void setNextState(StateId state)
    {
        stateMachine.setNextState(state);
    }
    
    IStateMachine& stateMachine;
}

class StateMachine : public IStateMachine
{
public:
    IState* getIStateFromId(StateId stateId)
    {
        case ID_STATEA:
        {
            return &statea;
        }

        case ID_STATEB:
        {
            return &stateb;
        }

        case ID_STATEC:
        {
            return &statec;
        }

        case ID_STATED:
        {
            return &stated;
        }
    }

    void update()
    {
        if (callEntry)
        {
          // only call entry once 
          istate->entry();
          callEntry = false;
        }
        istate->update();
    }

    void setNextState(StateId state)
    {
      this.istate = getIStateFromId(state);
      this.callEntry = true; // self transitions also call entry()
    }

private:
    StateId state;
    IState *istate;
    BOOL callEntry;

    StateA statea;
    StateB stateb;
    StateC statec;
    StateD stated;
}