import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-callback',
  imports: [CommonModule],
  templateUrl: './callback.html',
  styleUrl: './callback.css',
})
export class Callback implements OnInit {
  message = 'Logging you in...';

  constructor(private router: Router) {}

  ngOnInit() {
    // Read request_token from URL
    // Java analogy: @RequestParam("request_token")
    const params = new URLSearchParams(window.location.search);
    const requestToken = params.get('request_token');

    if (!requestToken) {
      this.message = '❌ No token found. Please try again.';
      return;
    }

    // Exchange request_token for access_token via FastAPI
    fetch(`${environment.apiUrl}/auth/callback?request_token=${requestToken}`)
      .then((res) => res.json())
      .then((data) => {
        // Store access_token in localStorage
        // Java analogy: HttpSession.setAttribute("access_token", token)
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user_name', data.user_name);

        this.message = `✅ Welcome ${data.user_name}! Redirecting...`;

        // Redirect to dashboard
        setTimeout(() => {
          this.router.navigate(['/dashboard']);
        }, 1500);
      })
      .catch((err) => {
        this.message = '❌ Login failed. Please try again.';
        console.error(err);
      });
  }
}
