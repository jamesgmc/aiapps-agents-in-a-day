using Microsoft.AspNetCore.Mvc;
using PsrGameServer.Models;
using PsrGameServer.Services;

namespace PsrGameServer.Controllers;

public class HomeController : Controller
{
    private readonly ITournamentService _tournamentService;

    public HomeController(ITournamentService tournamentService)
    {
        _tournamentService = tournamentService;
    }

    public IActionResult Index()
    {
        var tournament = _tournamentService.GetTournament();
        return View(tournament);
    }

    [HttpPost]
    public IActionResult StartTournament()
    {
        _tournamentService.StartTournament();
        return RedirectToAction("Index");
    }

    [HttpPost]
    public IActionResult EndTournament()
    {
        _tournamentService.EndTournament();
        return RedirectToAction("Index");
    }

    [HttpPost]
    public IActionResult StartRound(int roundNumber, string question, string correctAnswer)
    {
        if (string.IsNullOrWhiteSpace(question) || string.IsNullOrWhiteSpace(correctAnswer))
        {
            TempData["Error"] = "Question and correct answer are required";
        }
        else
        {
            var success = _tournamentService.StartRound(roundNumber, question, correctAnswer);
            if (!success)
            {
                TempData["Error"] = "Failed to start round";
            }
        }
        
        return RedirectToAction("Index");
    }

    [HttpPost]
    public IActionResult EndRound(int roundNumber)
    {
        var success = _tournamentService.EndRound(roundNumber);
        if (!success)
        {
            TempData["Error"] = "Failed to end round";
        }
        
        return RedirectToAction("Index");
    }

    public IActionResult Results()
    {
        var tournament = _tournamentService.GetTournament();
        return View(tournament);
    }

    public IActionResult Grid()
    {
        var tournament = _tournamentService.GetTournament();
        var viewModel = new GridViewModel
        {
            Players = tournament.Players,
            Rounds = tournament.Rounds.Where(r => r.Status == RoundStatus.Completed).ToList()
        };
        return View(viewModel);
    }
}

public class GridViewModel
{
    public List<Player> Players { get; set; } = new();
    public List<Round> Rounds { get; set; } = new();
}