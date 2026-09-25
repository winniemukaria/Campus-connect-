export default function Home() {
  return (
    <div style={{minHeight:'100vh', background:'#f8f9fa', textAlign:'center', fontFamily:'Arial', paddingBottom:'80px'}}>
      <h1 style={{paddingTop:'30px', fontSize:'28px', fontWeight:'bold'}}>CAMPUS CONNECT 🎓</h1>
      <p style={{color:'#666'}}>CEO Winnie Mukaria</p>

      {/* CEO CARD */}
      <div style={{background:'white', maxWidth:'380px', margin:'20px auto', padding:'25px', borderRadius:'18px', boxShadow:'0 4px 12px rgba(0,0,0,0.08)'}}>
        <div style={{width:'120px', height:'120px', borderRadius:'50%', margin:'0 auto', background:'#111', color:'white', display:'flex', alignItems:'center', justifyContent:'center', fontSize:'50px'}}>👑</div>
        <h2 style={{marginTop:'15px'}}>Winnie Mukaria</h2>
        <p style={{color:'#888', marginTop:'-10px'}}>Founder & CEO</p>
        <p style={{color:'#555', fontSize:'14px', marginTop:'10px'}}>Building the future of campus connection</p>
      </div>

      <h3>Our Staff</h3>
      <div style={{display:'flex', gap:'12px', justifyContent:'center', marginTop:'10px'}}>
        <div style={{background:'white', padding:'15px', borderRadius:'12px', width:'90px', boxShadow:'0 2px 8px rgba(0,0,0,0.06)'}}>👩‍💼<br/><small>Staff 1</small></div>
        <div style={{background:'white', padding:'15px', borderRadius:'12px', width:'90px', boxShadow:'0 2px 8px rgba(0,0,0,0.06)'}}>👨‍💼<br/><small>Staff 2</small></div>
        <div style={{background:'white', padding:'15px', borderRadius:'12px', width:'90px', boxShadow:'0 2px 8px rgba(0,0,0,0.06)'}}>👩‍💼<br/><small>Staff 3</small></div>
      </div>

      {/* ENTER BUTTON AT BOTTOM */}
      <a href="/select-role" style={{position:'fixed', bottom:'25px', left:'50%', transform:'translateX(-50%)', background:'black', color:'white', padding:'16px 70px', borderRadius:'30px', textDecoration:'none', fontWeight:'bold', fontSize:'18px', boxShadow:'0 4px 15px rgba(0,0,0,0.3)'}}>ENTER →</a>
    </div>
  )
}
