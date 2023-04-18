import React, { Component } from 'react';
import './PopupForm.css'
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { parse } from 'date-fns';
// import './DatePickerStyles.css';

class PopupForm extends Component {
  constructor(props) {
    super(props);

    this.state = {
      id: this.props.session.session_id,
      name: this.props.session.session_name,
      start_time:(this.props.session.session_start_time === undefined)?new Date(): parse(this.props.session.session_start_time, "yyyy-MM-dd HH:mm", new Date()),
      end_time: (this.props.session.session_end_time === undefined)?new Date():parse(this.props.session.session_end_time, "yyyy-MM-dd HH:mm", new Date()),
      camera_id:this.props.session.camera_id,
      cameras:[],
    };
  }

  componentDidMount(){
    fetch('http://localhost:5000/react/cameras')
      .then((response) => response.json())
      .then((data)=>this.setState({ cameras: data, camera_id: ((this.state.camera_id===undefined)?data[0].id:this.state.camera_id)}));
  }

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  handleDateStartChange = (date) =>{
    this.setState({ start_time: date });
  }

  handleDateEndChange = (date) =>{
    this.setState({ end_time: date });
  }

  handleCamChange = (cam) =>{
    console.log(cam.target.value)
    this.setState({camera_id: cam.target.value})
  }

  handleSubmit = () => {
    this.props.onSave({ ...this.state });
  };

  render() {
    const { name, start_time, end_time, cameras, camera_id } = this.state;
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
            <div className="datepicker-wrapper">
              <label htmlFor="start_time">Start time:</label>
              <DatePicker
                name='start_time'
                id='start_time'
                selected={start_time}
                onChange={(date) => this.handleDateStartChange(date)}
                showTimeSelect
                timeFormat="HH:mm"
                timeIntervals={15}
                dateFormat="yyyy-MM-dd HH:mm"
                timeCaption="time"
              />
            </div>
            <div className="datepicker-wrapper">
              <label htmlFor="end_time">End time:</label>
              <DatePicker
                name='end_time'
                id='end_time'
                selected={end_time}
                onChange={(date) => this.handleDateEndChange(date)}
                showTimeSelect
                timeFormat="HH:mm"
                timeIntervals={15}
                dateFormat="yyyy-MM-dd HH:mm"
                timeCaption="time"
              />
            </div>
            <div>
              <label htmlFor="className">Class name:</label>
              <select name="className" value={camera_id} onChange={(cam)=>this.handleCamChange(cam)}>
                {cameras.map((camera)=>(
                  <option key={camera.id} value={camera.id}>{camera.name}</option>
                ))}
              </select>
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
