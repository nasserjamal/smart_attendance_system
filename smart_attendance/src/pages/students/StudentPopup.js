import React, { Component } from 'react';
import './PopupForm.css'

class PopupForm extends Component {
  constructor(props) {
    super(props);

    this.state = {
      id: this.props.student.id,
      name: this.props.student.name,
      reg_no: this.props.student.reg_no,
    };
  }

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  handleSubmit = () => {
    this.props.onSave({ ...this.state });
  };

  render() {
    const { name, reg_no } = this.state;
    const { onCancel, onDelete } = this.props;

    return (
      <div className="popup">
        <div className="popup-content">
          <form>
            <div>
              <label htmlFor="name">Name:</label>
              <input
                type="text"
                id="name"
                name="name"
                value={name}
                onChange={this.handleChange}
              />
            </div>
            <div>
              <label htmlFor="reg_no">Registration Number:</label>
              <input
                type="text"
                id="reg_no"
                name="reg_no"
                value={reg_no}
                onChange={this.handleChange}
              />
            </div>
          </form>
          <button className="cancel" onClick={this.handleSubmit}>Save</button>
          <button className="cancel" onClick={onCancel}>Cancel</button>
          <button className="delete" onClick={onDelete}>Delete</button>
        </div>
      </div>
    );
  }
}

export default PopupForm;
