import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

interface Holding {
  ticker: string;
  quantity: number;
  avg_price: number;
  current_price: number;
  pnl: number;
  selected: boolean;
  status: 'not_analysed' | 'analysing' | 'analysed' | 'error';
  recommendation?: string;
  confidence?: string;
  technical_summary?: string;
  news_sentiment?: string;
  key_risks?: string;
  error_message?: string;
}

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {
  userName = '';
  accessToken = '';
  holdings: Holding[] = [];
  selectedHolding: Holding | null = null;
  loading = true;
  isAnalysing = false;
  error = '';

  // Scheduler UI state (no backend yet)
  schedulerEnabled = false;
  whatsappEnabled = false;
  analyseAllEnabled = false;

  constructor(private router: Router) {}

  ngOnInit() {
    this.accessToken = localStorage.getItem('access_token') || '';
    this.userName = localStorage.getItem('user_name') || '';

    if (!this.accessToken) {
      this.router.navigate(['/']);
      return;
    }

    this.loadHoldings();
  }

  loadHoldings() {
    this.loading = true;

    fetch(`http://127.0.0.1:8000/portfolio/holdings?access_token=${this.accessToken}`)
      .then((res) => res.json())
      .then((data) => {
        console.log('Holdings loaded:', data);
        this.holdings = data.holdings.map((h: any) => ({
          ...h,
          selected: false,
          status: 'not_analysed',
        }));
        this.loading = false;
      })
      .catch((err) => {
        this.error = 'Failed to load portfolio.';
        this.loading = false;
        console.error(err);
      });
  }

  // ── Selection ──────────────────────────────
  toggleSelect(holding: Holding) {
    if (holding.status === 'analysed' || holding.status === 'analysing') return;
    holding.selected = !holding.selected;
  }

  selectAll() {
    this.holdings.filter((h) => h.status === 'not_analysed').forEach((h) => (h.selected = true));
  }

  clearSelection() {
    this.holdings.forEach((h) => (h.selected = false));
  }

  get selectedCount(): number {
    return this.holdings.filter((h) => h.selected).length;
  }

  // ── Sections ───────────────────────────────
  get analysedHoldings(): Holding[] {
    return this.holdings.filter((h) => h.status === 'analysed');
  }

  get analysingHoldings(): Holding[] {
    return this.holdings.filter((h) => h.status === 'analysing');
  }

  get notAnalysedHoldings(): Holding[] {
    return this.holdings.filter((h) => h.status === 'not_analysed');
  }

  // ── Analysis loop ──────────────────────────
  async analyseSelected() {
    const toAnalyse = this.holdings.filter((h) => h.selected && h.status === 'not_analysed');
    if (toAnalyse.length === 0) return;

    this.isAnalysing = true;

    for (const holding of toAnalyse) {
      holding.status = 'analysing';
      holding.selected = false;

      console.log(`🤖 Analysing ${holding.ticker}...`);

      try {
        const res = await fetch(
          `http://127.0.0.1:8000/analysis/stock?ticker=${holding.ticker}&access_token=${this.accessToken}`,
        );
        const data = await res.json();
        console.log(`📦 ${holding.ticker}:`, data);

        if (data.status === 'error') {
          holding.status = 'error';
          holding.error_message = data.error_message || 'Unknown error';
        } else {
          holding.recommendation = data.recommendation;
          holding.confidence = data.confidence;
          holding.technical_summary = data.technical_summary;
          holding.news_sentiment = data.news_sentiment;
          holding.key_risks = data.key_risks;
          holding.status = 'analysed';

          if (!this.selectedHolding) {
            this.selectedHolding = holding;
          }
        }
      } catch (e) {
        console.error(`💥 ${holding.ticker} network error:`, e);
        holding.status = 'error';
      }
    }

    this.isAnalysing = false;
  }

  selectHolding(holding: Holding) {
    if (holding.status === 'analysed' || holding.status === 'error') {
      this.selectedHolding = holding;
    }
  }

  // ── Confidence helpers ─────────────────────
  getConfidenceNumber(holding: Holding | null): number {
    if (!holding) return 0;
    const raw = holding.confidence || '0';
    const match = raw.match(/\d+/);
    return match ? parseInt(match[0]) : 0;
  }

  getStrokeDashoffset(holding: Holding | null): number {
    const score = this.getConfidenceNumber(holding);
    return 188.5 - (score / 10) * 188.5;
  }

  getConfidenceColor(holding: Holding | null): string {
    const score = this.getConfidenceNumber(holding);
    if (score <= 4) return '#e53e3e';
    if (score <= 6) return '#d69e2e';
    return '#38a169';
  }

  getConfidenceLabel(holding: Holding | null): string {
    const score = this.getConfidenceNumber(holding);
    if (score <= 4) return 'Low confidence';
    if (score <= 6) return 'Medium confidence';
    return 'High confidence';
  }

  // ── Badge helpers ──────────────────────────
  getBadgeClass(rec: string | undefined): string {
    if (!rec) return 'badge-pending';
    const u = rec.toUpperCase();
    if (u.includes('BUY')) return 'badge-buy';
    if (u.includes('SELL')) return 'badge-sell';
    if (u.includes('HOLD')) return 'badge-hold';
    return 'badge-pending';
  }

  getPnlClass(pnl: number): string {
    return pnl >= 0 ? 'pnl-pos' : 'pnl-neg';
  }

  getShortName(ticker: string): string {
    return ticker.replace('.NS', '').replace('.BO', '');
  }

  get errorHoldings(): Holding[] {
    return this.holdings.filter((h) => h.status === 'error');
  }

  logout() {
    localStorage.clear();
    this.router.navigate(['/']);
  }
}
