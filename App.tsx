import { useState } from "react";

export default function App() {
  const [showRoles, setShowRoles] = useState(false);

  return (
    <div style={{minHeight:'100vh', background:'#f4f6fb', fontFamily:'Arial, sans-serif'}}>
      <div style={{background:'linear-gradient(135deg, #2457d6, #315fe0)', color:'white', textAlign:'center', padding:'40px 20px 55px'}}>
        <img src="/founder.jpg" alt="Founder" style={{width:'150px', height:'150px', borderRadius:'50%', objectFit:'cover', border:'5px solid #2563eb', display:'block', margin:'0 auto 18px'}} />
        <h1 style={{margin:0, fontSize:'30px'}}>Winnie Mukaria</h1>
        <div style={{display:'inline-block', marginTop:'12px', background:'#ff8a18', padding:'8px 18px', borderRadius:'25px', fontWeight:'bold'}}>👑 Founder & CEO</div>
        <p style={{marginTop:'18px', fontSize:'14px', fontWeight:'bold'}}>University of Embu • Year 1 • BCom • Email Notify ON</p>
        <div style={{maxWidth:'400px', margin:'20px auto 0', background:'rgba(255,255,255,0.18)', padding:'15px', borderRadius:'15px', textAlign:'left', lineHeight:'1.6', fontSize:'13px'}}>
          CampusConnect – Kenya's #1 student platform with EMAIL alerts! Students get email when new Job posted, Employers get email when CV uploaded. CEO gets all alerts.
        </div>
      </div>

      <div style={{width:'88%', maxWidth:'470px', margin:'-25px auto 40px', background:'white', borderRadius:'22px', padding:'28px 20px', textAlign:'center', boxShadow:'0 8px 25px rgba(0,0,0,0.08)'}}>
        <h2 style={{margin:0, color:'#25477b', fontSize:'23px'}}>Welcome to CampusConnect</h2>
        <p style={{color:'#777', marginTop:'8px', fontSize:'13px'}}>Founded by Winnie Mukaria</p>
        
        <button onClick={() => { setShowRoles(true); setTimeout(()=>{document.getElementById("roles")?.scrollIntoView({behavior:'smooth'})},200) }} style={{width:'100%', marginTop:'18px', padding:'17px', border:'none', borderRadius:'15px', background:'#ff7a16', color:'white', fontWeight:'bold', fontSize:'16px', cursor:'pointer'}}>
          Enter CampusConnect →
        </button>
        <p style={{fontSize:'10px', color:'#aaa', marginTop:'12px'}}>📧 Email notifications + M-Pesa 0705991406</p>
      </div>

      {showRoles && (
        <div id="roles" style={{width:'90%', maxWidth:'470px', margin:'0 auto 60px', textAlign:'center'}}>
          <h2 style={{color:'#25477b'}}>Choose Your Role</h2>
          <a href="https://campusconnect.indevs.in" style={{display:'block', background:'white', padding:'20px', margin:'15px 0', borderRadius:'15px', textDecoration:'none', color:'#2457d6', fontWeight:'bold', border:'2px solid #dbeafe'}}>🎓 I'm a Student</a>
          <a href="https://campusconnect.indevs.in" style={{display:'block', background:'white', padding:'20px', margin:'15px 0', borderRadius:'15px', textDecoration:'none', color:'#ff7a16', fontWeight:'bold', border:'2px solid #fed7aa'}}>💼 I'm an Employer</a>
        </div>
      )}
    </div>
  );
}
