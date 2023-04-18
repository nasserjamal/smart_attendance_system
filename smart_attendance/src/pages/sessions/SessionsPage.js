import React from 'react';
import PopupForm from './SessionPopup';
import ReportsPopup from './reportsPopup';

class SessionsPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sessions: [],
      isPopupVisible: false,
      selectedSession: '',
      isReportsPopupVisible: false,
    };
  }

  componentDidMount() {
    fetch('http://localhost:5000/react/sessions')
      .then((response) => response.json())
      .then((data)=>this.setState({ sessions: data }));
  }

  isStartTimePast = (startTime) => {
    const currentTime = new Date();
    const sessionStartTime = new Date(startTime);
    return sessionStartTime < currentTime;
  };

  handleViewReports = (session) => {
    this.setState({ selectedSession: session, isReportsPopupVisible: true });
  };

  handleCloseReports = () => {
    this.setState({ isReportsPopupVisible: false });
  };

  handleAddSession = () => {
    this.setState({ selectedSession: '',isPopupVisible: true });
  };

  handleEditSession = (session) => {
    this.setState({ isPopupVisible: true, selectedSession: session});
  };

  async newSession(session){
    console.log(session)
    try {
      const response = await fetch('http://localhost:5000/react/session/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(session),
      });

      if (response.ok) {
        this.setState({ isPopupVisible: false });
        window.location.reload();
      } else {
        console.log(`Error: ${response.statusText}`);
      }
    } catch (error) {
      console.log(`Error: ${error.message}`);
    }
  }

  handleSave = async (session) => {
    if (session.id === undefined){
      this.newSession(session);
      return;
    }

    try {
      const response = await fetch('http://192.168.20.42.:5000/react/session/'+session.id, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(session),
      });

      if (response.ok) {
        this.setState({ isPopupVisible: false });
        window.location.reload();
      } else {
        console.log(`Error: ${response.statusText}`);
      }
    } catch (error) {
      console.log(`Error: ${error.message}`);
    }
  };

  handleCancel = () => {
    console.log('Cancel');
    this.setState({ isPopupVisible: false });
  };

  handleDelete = async (session) => {
    try {
        console.log("Now deleting: "+this.state.selectedSession.session_id)
        const response = await fetch('http://localhost:5000/react/session/'+this.state.selectedSession.session_id, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (response.ok) {
        this.setState({ isPopupVisible: false });
        window.location.reload();
      } else {
        console.log(`Error: ${response.statusText}`);
      }
    } catch (error) {
      console.log(`Error: ${error.message}`);
    }
  };

  render() {
    const { sessions, isPopupVisible, selectedSession, isReportsPopupVisible } = this.state;

    return (
      <div>
        <div><button onClick={this.handleAddSession}>Add Session</button></div>
        <h1>Sessions</h1>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Session Name</th>
              <th>Class name</th>
              <th>Start time</th>
              <th>End time</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {sessions.map((session) => (
              <tr key={session.session_id}>
                <td>{session.session_id}</td>
                <td>{session.session_name}</td>
                <td>{session.camera_name}</td>
                <td>{session.session_start_time}</td>
                <td>{session.session_end_time}</td>
                <td>
                {this.isStartTimePast(session.session_start_time) ? (
                  <button onClick={() => this.handleViewReports(session)}>
                    View Reports
                  </button>
                ) : (
                  <button onClick={() => this.handleEditSession(session)}>
                    Edit
                  </button>
                )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {isPopupVisible && (
          <PopupForm
            onSave={this.handleSave}
            onCancel={this.handleCancel}
            onDelete={this.handleDelete}
            session={selectedSession}
          />
        )}

        {isReportsPopupVisible && (
          <ReportsPopup
            onClose={this.handleCloseReports}
            session={selectedSession}
          />
        )}
      </div>
    );
  }
}

export default SessionsPage;
