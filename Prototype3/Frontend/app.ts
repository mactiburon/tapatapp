const API_URL = "http://localhost:5000";  // URL de tu backend

// Elementos del DOM
const loginForm = document.getElementById("login-form") as HTMLDivElement;
const content = document.getElementById("content") as HTMLDivElement;
const emailInput = document.getElementById("email") as HTMLInputElement;
const passwordInput = document.getElementById("password") as HTMLInputElement;
const loginMessage = document.getElementById("login-message") as HTMLParagraphElement;
const childrenList = document.getElementById("children-list") as HTMLUListElement;
const historialMessage = document.getElementById("historial-message") as HTMLParagraphElement;

// Función para iniciar sesión
async function login() {
    const email = emailInput.value;
    const password = passwordInput.value;

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("user", JSON.stringify(data.user));
            showContent();
        } else {
            loginMessage.textContent = data.error || "Error al iniciar sesión";
        }
    } catch (error) {
        loginMessage.textContent = "Error de conexión";
    }
}

// Función para mostrar el contenido después del login
function showContent() {
    loginForm.style.display = "none";
    content.style.display = "block";
    loadChildren();
}

// Función para cargar la lista de niños
async function loadChildren() {
    try {
        const token = localStorage.getItem("access_token");
        const response = await fetch(`${API_URL}/children`, {
            headers: { "Authorization": `Bearer ${token}` },
        });

        const children = await response.json();
        childrenList.innerHTML = "";

        children.forEach((child: any) => {
            const li = document.createElement("li");
            li.textContent = `${child.child_name} - ${child.informacioMedica}`;
            childrenList.appendChild(li);
        });
    } catch (error) {
        console.error("Error al cargar niños:", error);
    }
}

// Función para añadir un historial
async function addHistorial() {
    const childName = (document.getElementById("child-name") as HTMLInputElement).value;
    const date = (document.getElementById("historial-date") as HTMLInputElement).value;
    const time = (document.getElementById("historial-time") as HTMLInputElement).value;
    const estat = (document.getElementById("historial-estat") as HTMLInputElement).value;
    const horas = (document.getElementById("historial-horas") as HTMLInputElement).value;

    try {
        const token = localStorage.getItem("access_token");
        const response = await fetch(`${API_URL}/medicos/historial`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({
                child_id: 1,  // Cambia esto según tu lógica
                data: date,
                hora: time,
                estat,
                totalHores: horas,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            historialMessage.textContent = "Historial añadido correctamente";
            loadChildren();
        } else {
            historialMessage.textContent = data.error || "Error al añadir historial";
        }
    } catch (error) {
        historialMessage.textContent = "Error de conexión";
    }
}

// Verificar si el usuario ya está logueado
window.onload = () => {
    const token = localStorage.getItem("access_token");
    if (token) {
        showContent();
    }
};