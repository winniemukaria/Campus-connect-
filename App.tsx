import { useState } from 'react'

export default function App() {
  const [page, setPage] = useState('home')
  const [role, setRole] = useState('')

  if (page === 'home') {
    return (
      <div style={{minHeight:'100vh', background:'#f8f9fa', textAlign:'center', fontFamily:'Arial', paddingBottom:'90px'}}>
        <h1 style={{paddingTop:'30px'}}>CAMPUS CONNECT 🎓</h1>
        <p style={{color:'#666'}}>CEO Winnie Mukaria</p>
        <div style={{background:'white', maxWidth:'360px', margin:'20px auto', padding:'20px', borderRadius:'15px'}}>
          <div style={{width:'110px', height:'110px', background:'black', color:'white', borderRadius:'50%', margin:'0 auto', display:'flex', alignItems:'center', justifyContent:'center', fontSize:'45px'}}>👑</div>
          <h2>Winnie Mukaria</h2>
          <p style={{color:'#888'}}>Founder</p>
        </div>
        <div style={{display:'flex', gap:'10px', justifyContent:'center'}}>
          <div style={{background:'white', padding:'12px', borderRadius:'10px', width:'80px'}}>👩‍💼<br/><small>Staff</small></div>
          <div style={{background:'white', padding:'12px', borderRadius:'10px', width:'80px'}}>👨‍💼<br/><small>Staff</small></div>
          <div style={{background:'white', padding:'12px', borderRadius:'10px', width:'80px'}}>👩‍💼<br/><small>Staff</small></div>
        </div>
        <button onClick={()=>setPage('role')} style={{position:'fixed', bottom:'20px', left:'50%', transform:'translateX(-50%)', background:'black', color:'white', padding:'16px 65px', borderRadius:'30px', border:'none', fontWeight:'bold', fontSize:'18px'}}>ENTER →</button>
      </div>
    )
  }

  if (page === 'role') {
    return (
      <div style={{minHeight:'100vh', background:'#f8f9fa', textAlign:'center', paddingTop:'50px', fontFamily:'Arial'}}>
        <h2>Welcome</h2>
        <p style={{color:'#666'}}>Choose to continue</p>
        <div style={{maxWidth:'360px', margin:'30px auto', display:'flex', flexDirection:'column', gap:'15px', padding:'20px'}}>
          <button onClick={()=>{setRole('student'); setPage('signup')}} style={{background:'white', padding:'20px', borderRadius:'15px', border:'2px solid #e0e0e0'}}>
            <div style={{fontSize:'35px'}}>🎓</div><h3>I'm a Student</h3>
          </button>
          <button onClick={()=>{setRole('employer'); setPage('signup')}} style={{background:'white', padding:'20px', borderRadius:'15px', border:'2px solid #e0e0e0'}}>
            <div style={{fontSize:'35px'}}>💼</div><h3>I'm an Employer</h3>
          </button>
        </div>
      </div>
    )
  }

  return (
    <div style={{minHeight:'100vh', background:'#f8f9fa', textAlign:'center', paddingTop:'60px', fontFamily:'Arial'}}>
      <h2>{role === 'student' ? 'Student' : 'Employer'} Signup</h2>
      <p style={{color:'#666'}}>Create account to access features</p>
      <div style={{background:'white', maxWidth:'360px', margin:'20px auto', padding:'20px', borderRadius:'15px'}}>
        <input placeholder="Full Name" style={{width:'90%', padding:'12px', margin:'8px 0', borderRadius:'8px', border:'1px solid #ddd'}}/>
        <input placeholder="Email" style={{width:'90%', padding:'12px', margin:'8px 0', borderRadius:'8px', border:'1px solid #ddd'}}/>
        <input placeholder="Password" type="password" style={{width:'90%', padding:'12px', margin:'8px 0', borderRadius:'8px', border:'1px solid #ddd'}}/>
        <button onClick={()=>window.location.href='https://campusconnect.indevs.in'} style={{width:'95%', background:'black', color:'white', padding:'14px', borderRadius:'25px', border:'none', marginTop:'15px', fontWeight:'bold'}}>CREATE ACCOUNT & ENTER</button>
      </div>
    </div>
  )
        }
