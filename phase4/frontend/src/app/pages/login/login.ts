import { Component } from '@angular/core';

@Component({
  selector: 'app-login',
  imports: [],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  loginWithZerodha() {
    // Call FastAPI to get Zerodha login URL
    // then redirect user to it
    fetch('http://127.0.0.1:8000/auth/login')
      .then((res) => res.json())
      .then((data) => {
        // Redirect browser to Zerodha login page
        // Java analogy: response.sendRedirect(url)
        window.location.href = data.login_url;
      })
      .catch((err) => {
        console.error('Failed to get login URL:', err);
        alert('Failed to connect to FinVeda backend. Is it running?');
      });
  }
}
