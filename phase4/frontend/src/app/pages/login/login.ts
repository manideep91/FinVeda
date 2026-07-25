import { Component } from '@angular/core';
import { environment } from '../../../environments/environment';

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
    fetch(`${environment.apiUrl}/auth/login`)
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
