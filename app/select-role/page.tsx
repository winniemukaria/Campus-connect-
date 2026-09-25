export default function SelectRole() {
  return (
    <div style={{minHeight:'100vh', background:'#f8f9fa', textAlign:'center', fontFamily:'Arial', paddingTop:'50px'}}>
      <h2>Welcome to Campus Connect</h2>
      <p style={{color:'#666'}}>Choose how you want to continue</p>
      
      <div style={{maxWidth:'380px', margin:'30px auto', display:'flex', flexDirection:'column', gap:'15px', padding:'20px'}}>
        <a href="/signup?role=student" style={{background:'white', padding:'20px', borderRadius:'15px', textDecoration:'none', color:'black', boxShadow:'0 2px 10px rgba(0,0,0,0.08)', border:'2px solid #e0e0e0'}}>
          <div style={{fontSize:'40px'}}>🎓</div>
          <h3>I'm a Student</h3>
          <p style={{color:'#888', fontSize:'14px'}}>Access classes, attendance, ID card</p>
        </a>
        
        <a href="/signup?role=employer" style={{background:'white', padding:'20px', borderRadius:'15px', textDecoration:'none', color:'black', boxShadow:'0 2px 10px rgba(0,0,0,0.08)', border:'2px solid #e0e0e0'}}>
          <div style={{fontSize:'40px'}}>💼</div>
          <h3>I'm an Employer</h3>
          <p style={{color:'#888', fontSize:'14px'}}>Post jobs, find students</p>
        </a>
      </div>
    </div>
  )
}
