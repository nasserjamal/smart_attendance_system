import React from 'react';
import PopupForm from './StudentPopup';

class StudentsPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      students: [],
      isPopupVisible: false,
      selectedStudent: '',
    };
  }

  componentDidMount() {
    fetch('http://localhost:5000/react/students')
      .then((response) => response.json())
      .then((data)=>this.setState({ students: data }));
  }

  handleAddStudent = () => {
    this.setState({ isPopupVisible: true });
  };

  handleEditStudent = (student) => {
    this.setState({ isPopupVisible: true, selectedStudent: student});
  };

  handleSave = async (student) => {
    try {
      const response = await fetch('http://localhost:5000/react/student', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(student),
      });

      if (response.ok) {
        this.setState({ isPopupVisible: false });
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

  handleDelete = async (student) => {
    try {
      const response = await fetch('http://localhost:5000/react/student/'+this.state.selectedStudent.id, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (response.ok) {
        this.setState({ isPopupVisible: false });
      } else {
        console.log(`Error: ${response.statusText}`);
      }
    } catch (error) {
      console.log(`Error: ${error.message}`);
    }
  };

  render() {
    const { students, isPopupVisible, selectedStudent } = this.state;

    return (
      <div>
        <div><button onClick={this.handleAddStudent}>Add Student</button></div>
        <h1>Students</h1>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Registration no</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {students.map((student) => (
              <tr key={student.id}>
                <td>{student.id}</td>
                <td>{student.name}</td>
                <td>{student.reg_no}</td>
                <td><button onClick={()=>this.handleEditStudent(student)}>Edit</button></td>
              </tr>
            ))}
          </tbody>
        </table>

        {isPopupVisible && (
          <PopupForm
            onSave={this.handleSave}
            onCancel={this.handleCancel}
            onDelete={this.handleDelete}
            student={selectedStudent}
          />
        )}
      </div>
    );
  }
}

export default StudentsPage;
