import logging

import typer

from .ingest.backfill import run_backfill

app = typer.Typer()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.command()
def ingest(start: str, end: str):
    """Backfill MCX Bhavcopy data from start to end dates."""
    typer.echo(f"Starting ingestion from {start} to {end}")
    run_backfill(start, end)
    typer.echo("Ingestion complete.")

@app.command()
def build():
    """Build analytics artifacts and term structures."""
    typer.echo("Building carry curves and artifacts...")
    # Placeholder for actual build logic
    
@app.command()
def backtest(confirm_holdout: bool = typer.Option(False, "--confirm-holdout", help="Unlock the holdout set")):
    """Run walk-forward backtest."""
    typer.echo(f"Running backtest... (Holdout unlocked: {confirm_holdout})")
    
@app.command()
def verdict():
    """Generate final verdict report."""
    typer.echo("Generating verdict...")
    
@app.command()
def alerts():
    """Run alert engine on latest data."""
    typer.echo("Evaluating alerts...")

@app.command()
def demo():
    """Run the 3-minute offline demo script on synthetic/sample data."""
    typer.echo("Running demo...")

if __name__ == "__main__":
    app()
