export default function App() {
  return (
    <div style={{minHeight:'100vh',background:'#f8fafc',fontFamily:'Arial',textAlign:'center',paddingBottom:'120px'}}>
      <h1 style={{paddingTop:'30px'}}>CAMPUS CONNECT 🎓</h1>
      <p>CEO Winnie Mukaria</p>
      
      <div style={{background:'white',width:'90%',maxWidth:'350px',margin:'20px auto',padding:'20px',borderRadius:'20px',boxShadow:'0 4px 12px rgba(0,0,0,.08)'}}>
        <img src="/founder.jpg" alt="Winnie Mukaria CEO" style={{width:'120px',height:'120px',borderRadius:'50%',objectFit:'cover',margin:'0 auto',display:'block',border:'3px solid black'}} />
        <h2 style={{marginTop:'15px'}}>Winnie Mukaria</h2>
        <p style={{color:'#888',margin:'5px 0'}}>Founder & CEO</p>
      </div>

      <div style={{display:'flex',gap:'10px',justifyContent:'center',marginTop:'10px'}}>
        <div style={{background:'white',padding:'10px',borderRadius:'10px',width:'70px',boxShadow:'0 2px 6px rgba(0,0,0,.05)'}}>👩‍💼<br/><small>Staff</small></div>
        <div style={{background:'white',padding:'10px',borderRadius:'10px',width:'70px',boxShadow:'0 2px 6px rgba(0,0,0,.05)'}}>👨‍💼<br/><small>Staff</small></div>
        <div style={{background:'white',padding:'10px',borderRadius:'10px',width:'70px',boxShadow:'0 2px 6px rgba(0,0,0,.05)'}}>👩‍💼<br/><small>Staff</small></div>
      </div>

      <a href="#roles" style={{position:'fixed',bottom:'20px',left:'50%',transform:'translateX(-50%)',background:'black',color:'white',padding:'16px 65px',borderRadius:'30px',textDecoration:'none',fontWeight:'bold',fontSize:'18px'}}>ENTER →</a>

      <div id="roles" style={{marginTop:'90px',padding:'20px'}}>
        <h2>Choose Your Role</h2>
        <p style={{color:'#666'}}>Continue to features</p>
        <a href="https://campusconnect.indevs.in" style={{display:'block',background:'white',margin:'15px auto',padding:'20px',maxWidth:'300px',borderRadius:'15px',textDecoration:'none',color:'black',fontWeight:'bold',boxShadow:'0 2px 8px rgba(0,0,0,.06)'}}>🎓 I'm a Student</a>
        <a href="https://campusconnect.indevs.in" style={{display:'block',background:'white',margin:'15px auto',padding:'20px',maxWidth:'300px',borderRadius:'15px',textDecoration:'none',color:'black',fontWeight:'bold',boxShadow:'0 2px 8px rgba(0,0,0,.06)'}}>💼 I'm an Employer</a>
      </div>
    </div>
  )
}
