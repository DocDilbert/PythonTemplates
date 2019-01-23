
enum StateId
{
  ID_STATEA
  ID_STATEB
}

class IStateMachine
{
  public:
  	virtual void setNextState(StateId state) = 0;
}


class IState 
{
  public:
    virtual State getId() = 0;
    virtual void update() = 0;
}


class StateA : public IState
{
public:
    StateId getId()
    {
        return ID_STATEA;
    }

    void update()
    {
        // Check for transitions here ...
    }

    void setNextState(StateId state)
    {
        stateMachine.setNextState(state);
    }

private:
    IStateMachine& stateMachine;
}

class StateB : public IState
{
public:
    StateId getId()
    {
        return ID_STATEB;
    }

    void update()
    {
        // Check for transitions here ...
    }

    void setNextState(StateId state)
    {
        stateMachine.setNextState(state);
    }

private:
    IStateMachine& stateMachine;
}

