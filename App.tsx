export default function App() {
  return (
    <div style={{minHeight:'100vh',background:'#f8fafc',fontFamily:'Arial',textAlign:'center',paddingBottom:'100px'}}>
      <h1 style={{paddingTop:'30px'}}>CAMPUS CONNECT 🎓</h1>
      <p>CEO Winnie Mukaria</p>
      <div style={{background:'white',width:'90%',maxWidth:'350px',margin:'20px auto',padding:'20px',borderRadius:'20px'}}>
        <div style={{width:'100px',height:'100px',background:'#000',color:'#fff',borderRadius:'50%',margin:'0 auto',display:'flex',alignItems:'center',justifyContent:'center',fontSize:'40px'}}>W</div>
        <h2>Winnie Mukaria</h2><p style={{color:'#888'}}>Founder & CEO</p>
      </div>
      <div style={{display:'flex',gap:'10px',justifyContent:'center'}}>
        <div style={{background:'white',padding:'10px',borderRadius:'10px',width:'70px'}}>Staff</div>
        <div style={{background:'white',padding:'10px',borderRadius:'10px',width:'70px'}}>Staff</div>
        <div style={{background:'white',padding:'10px',borderRadius:'10px',width:'70px'}}>Staff</div>
      </div>
      <a href="#roles" style={{position:'fixed',bottom:'20px',left:'50%',transform:'translateX(-50%)',background:'black',color:'white',padding:'15px 60px',borderRadius:'30px',textDecoration:'none',fontWeight:'bold'}}>ENTER →</a>
      <div id="roles" style={{marginTop:'100px',padding:'20px'}}>
        <h2>Choose Role</h2>
        <a href="https://campusconnect.indevs.in" style={{display:'block',background:'white',margin:'15px auto',padding:'20px',maxWidth:'300px',borderRadius:'15px',textDecoration:'none',color:'black',fontWeight:'bold'}}>🎓 I'm a Student</a>
        <a href="https://campusconnect.indevs.in" style={{display:'block',background:'white',margin:'15px auto',padding:'20px',maxWidth:'300px',borderRadius:'15px',textDecoration:'none',color:'black',fontWeight:'bold'}}>💼 I'm an Employer</a>
      </div>
    </div>
  )
}
