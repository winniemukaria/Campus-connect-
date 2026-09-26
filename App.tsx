import { useEffect, useState } from "react";

export default function App() {
  const [showRoles, setShowRoles] = useState(false);

  useEffect(() => {
    const handleEnter = (event: KeyboardEvent) => {
      if (event.key === "Enter") {
        setShowRoles(true);

        setTimeout(() => {
          document.getElementById("roles")?.scrollIntoView({
            behavior: "smooth",
          });
        }, 50);
      }
    };

    window.addEventListener("keydown", handleEnter);

    return () => {
      window.removeEventListener("keydown", handleEnter);
    };
  }, []);

  const enterCampusConnect = () => {
    setShowRoles(true);

    setTimeout(() => {
      document.getElementById("roles")?.scrollIntoView({
        behavior: "smooth",
      });
    }, 50);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#eff6ff",
        fontFamily: "Arial, sans-serif",
        textAlign: "center",
        paddingBottom: "100px",
      }}
    >
      {/* BRANDING */}
      <h1
        style={{
          paddingTop: "30px",
          color: "#1e40af",
          fontSize: "28px",
          fontWeight: "bold",
          marginBottom: "5px",
        }}
      >
        CAMPUS CONNECT 🎓
      </h1>

      <p
        style={{
          color: "#f97316",
          fontWeight: "bold",
          marginTop: "0",
        }}
      >
        Connecting Students to Opportunities
      </p>

      {/* FOUNDER CARD */}
      <div
        style={{
          background: "white",
          width: "90%",
          maxWidth: "360px",
          margin: "25px auto",
          padding: "25px",
          borderRadius: "20px",
          boxShadow: "0 8px 20px rgba(0,0,0,.08)",
          border: "2px solid #dbeafe",
          boxSizing: "border-box",
        }}
      >
        <img
          src="/founder.jpg"
          alt="Winnie Mukaria"
          style={{
            width: "130px",
            height: "130px",
            borderRadius: "50%",
            objectFit: "cover",
            margin: "0 auto",
            display: "block",
            border: "4px solid #2563eb",
            boxShadow: "0 0 0 4px #fed7aa",
          }}
        />

        <h2
          style={{
            marginTop: "15px",
            marginBottom: "5px",
            color: "#1e293b",
          }}
        >
          Winnie Mukaria
        </h2>

        <p
          style={{
            color: "#2563eb",
            fontWeight: "bold",
            margin: "0",
          }}
        >
          Founder & CEO
        </p>

        <p
          style={{
            color: "#64748b",
            fontSize: "14px",
            marginTop: "10px",
          }}
        >
          Building the future for students in Kenya and beyond
        </p>

        {/* TEAM */}
        <div
          style={{
            display: "flex",
            gap: "10px",
            justifyContent: "center",
            marginTop: "20px",
          }}
        >
          <div
            style={{
              background: "#eff6ff",
              padding: "10px",
              borderRadius: "12px",
              width: "75px",
              border: "1px solid #bfdbfe",
            }}
          >
            👩‍💼
            <br />
            <small style={{ color: "#1e40af" }}>Staff</small>
          </div>

          <div
            style={{
              background: "#fff7ed",
              padding: "10px",
              borderRadius: "12px",
              width: "75px",
              border: "1px solid #fed7aa",
            }}
          >
            👨‍💼
            <br />
            <small style={{ color: "#f97316" }}>Staff</small>
          </div>

          <div
            style={{
              background: "#eff6ff",
              padding: "10px",
              borderRadius: "12px",
              width: "75px",
              border: "1px solid #bfdbfe",
            }}
          >
            👩‍💼
            <br />
            <small style={{ color: "#1e40af" }}>Staff</small>
          </div>
        </div>
      </div>

      {/* ENTER BUTTON */}
      {!showRoles && (
        <button
          onClick={enterCampusConnect}
          type="button"
          style={{
            position: "fixed",
            bottom: "20px",
            left: "50%",
            transform: "translateX(-50%)",
            background: "#f97316",
            color: "white",
            padding: "16px 70px",
            borderRadius: "30px",
            border: "none",
            fontWeight: "bold",
            fontSize: "18px",
            boxShadow: "0 4px 15px rgba(249,115,22,.4)",
            cursor: "pointer",
            zIndex: 1000,
          }}
        >
          ENTER →
        </button>
      )}

      {/* ROLE SELECTION */}
      {showRoles && (
        <div
          id="roles"
          style={{
            marginTop: "60px",
            padding: "20px",
          }}
        >
          <h2 style={{ color: "#1e40af" }}>Choose Your Role</h2>

          <p style={{ color: "#64748b" }}>
            Select how you want to continue
          </p>

          <a
            href="https://campusconnect.indevs.in"
            style={{
              display: "block",
              background: "white",
              margin: "15px auto",
              padding: "20px",
              maxWidth: "320px",
              borderRadius: "15px",
              textDecoration: "none",
              color: "#1e40af",
              fontWeight: "bold",
              border: "2px solid #dbeafe",
            }}
          >
            🎓 I'm a Student
          </a>

          <a
            href="https://campusconnect.indevs.in"
            style={{
              display: "block",
              background: "white",
              margin: "15px auto",
              padding: "20px",
              maxWidth: "320px",
              borderRadius: "15px",
              textDecoration: "none",
              color: "#f97316",
              fontWeight: "bold",
              border: "2px solid #fed7aa",
            }}
          >
            💼 I'm an Employer
          </a>
        </div>
      )}
    </div>
  );
}
