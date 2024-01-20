import React, { useState } from 'react'
import OrganizationLogin from './OrganizationLogin'
import OrganizationSignup from './OrganizationSignup'

function Organization() {
    const [Obooleanvalue, setOBoolean] = useState(true);
  return (
    <>
      <section className="bg-primary py-3 py-md-5 py-xl-8">
        <div className="container">
          <div className="row gy-4 align-items-center">
          {Obooleanvalue ? (<div className="col-12 col-md-6 col-xl-7">
              <div className="d-flex justify-content-center text-bg-primary">
                <div className="col-12 col-xl-9">
                  <hr className="border-primary-subtle mb-4" />
                  <h2 className="h1 mb-4">You can Share your Wonderful Upcoming Event To the User</h2>
                  <p className="lead mb-5">So User can be the Part of your Wonderful Event's Memory</p>
                  <div className="text-endx">
                  </div>
                </div>
              </div>
            </div>) : (<div className="col-12 col-md-6 col-xl-5">
              <div className="d-flex justify-content-center text-bg-primary">
                <div className="col-12 col-xl-9">
                  <hr className="border-primary-subtle mb-4" />
                  <h2 className="h1 mb-4">You can Share your Wonderful Upcoming Event To the User</h2>
                  <p className="lead mb-5">So User can be the Part of your Wonderful Event's Memory</p>
                  <div className="text-endx">
                  </div>
                </div>
              </div>
            </div>)}
            {/* <div className="col-12 col-md-6 col-xl-7">
              <div className="d-flex justify-content-center text-bg-primary">
                <div className="col-12 col-xl-9">
                  <hr className="border-primary-subtle mb-4" />
                  <h2 className="h1 mb-4">You can Share your Wonderful Upcoming Event To the User</h2>
                  <p className="lead mb-5">So User can be the Part of your Wonderful Event's Memory</p>
                  <div className="text-endx">
                  </div>
                </div>
              </div>
            </div> */}
            {Obooleanvalue ? <OrganizationLogin setOBoolean={setOBoolean} /> : <OrganizationSignup setOBoolean={setOBoolean} />}
          </div>
        </div>
      </section>
    </>
  )
}

export default Organization