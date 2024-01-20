import React, { useState } from 'react'
import api from "../../../api"

function UserSignup({ setUBoolean }) {
    const [lFormData, setLFormData] = useState({
        name: "",
        email: "",
        pnumber: '',
        gender: "",
        username: "",
        pwd: "",
    });

    const handleInputChange = (event) => {
        setLFormData({
            ...lFormData,
            [event.target.name]: event.target.value,
        });
    };

    const handleFormSubmit = async (event) => {
        event.preventDefault();
        try {
            await api.post("/usersignup/", lFormData);

            setLFormData({
                name: "",
                email: "",
                pnumber: '',
                gender: "",
                username: "",
                pwd: "",
            });
        } catch (error) {
            console.error("Error submitting form:", error);
        }
    };
    return (
        <>
            <div className="col-12 col-md-6 col-xl-5">
                <div className="card border-0 rounded-4">
                    <div className="card-body p-3 p-md-4 p-xl-5">
                        <div className="row">
                            <div className="col-12">
                                <div className="mb-4">
                                    <h3>User Sign up</h3>
                                    <p>if you have an account? <button className='btn btn-primary' onClick={() => {
                                        setUBoolean(true)
                                    }}>Login</button></p>
                                </div>
                            </div>
                        </div>
                        <form onSubmit={handleFormSubmit}>
                            <div className="row gy-3 overflow-hidden">
                                <div className="col-12">
                                    <div className="form-floating">
                                        <input
                                            type="text"
                                            className="form-control"
                                            id="name"
                                            placeholder=" "
                                            name="name"
                                            value={lFormData.name}
                                            onChange={handleInputChange}
                                        />
                                        <label htmlFor="name" className="form-label">
                                            Name
                                        </label>
                                    </div>
                                </div>
                                <div className="col-12">
                                    <div className="form-floating">
                                        <input
                                            type="email"
                                            className="form-control"
                                            id="email"
                                            placeholder=""
                                            name="email"
                                            value={lFormData.email}
                                            onChange={handleInputChange}
                                        />
                                        <label htmlFor="email" className="form-label">
                                            Email
                                        </label>
                                    </div>
                                </div>
                                <div className="col-12">
                                    <div className="form-floating">
                                        <input
                                            type="number"
                                            className="form-control"
                                            id="pnumber"
                                            placeholder=""
                                            name="pnumber"
                                            value={lFormData.pnumber}
                                            onChange={handleInputChange}
                                        />
                                        <label htmlFor="pnumber" className="form-label">
                                            Phone Number
                                        </label>
                                    </div>
                                </div>
                                <div className="col-12">
                                    <div className="">
                                        <label htmlFor="gender" className="form-label me-3">
                                            Gender
                                        </label>
                                        <input
                                            type="radio"
                                            name="gender"
                                            value="Male"
                                            checked={lFormData.gender === "Male"}
                                            onChange={handleInputChange}
                                        />
                                        Male
                                        <input
                                            type="radio"
                                            name="gender"
                                            value="Female"
                                            checked={lFormData.gender === "Female"}
                                            className='ms-2'
                                            onChange={handleInputChange}
                                        />
                                        Female
                                    </div>
                                </div>
                                <div className="col-12">
                                    <div className="form-floating">
                                        <input
                                            type="text"
                                            className="form-control"
                                            id="username"
                                            placeholder="Enter your user name"
                                            name="username"
                                            value={lFormData.username}
                                            onChange={handleInputChange}
                                        />
                                        <label htmlFor="username" className="form-label">
                                            Username:
                                        </label>
                                    </div>
                                </div>
                                <div className="col-12">
                                    <div className="form-floating">
                                        <input
                                            type="password"
                                            className="form-control"
                                            id="pwd"
                                            placeholder="Enter your password"
                                            name="pwd"
                                            value={lFormData.pwd}
                                            onChange={handleInputChange}
                                        />
                                        <label htmlFor="pwd" className="form-label">
                                            Password:
                                        </label>
                                    </div>
                                </div>
                                <div className="col-12">
                                    <div className="d-grid">
                                        <button className="btn btn-primary btn-lg" type="submit">Log in now</button>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </>

    )
}

export default UserSignup