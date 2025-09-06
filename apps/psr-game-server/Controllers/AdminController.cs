using Microsoft.AspNetCore.Mvc;
using PsrGameServer.Models;
using PsrGameServer.Services;

namespace PsrGameServer.Controllers;

public class AdminController : Controller
{
    private readonly ITournamentService _tournamentService;
    private const string AdminPasscode = "9999";
    private const string AdminSessionKey = "AdminAuthenticated";

    public AdminController(ITournamentService tournamentService)
    {
        _tournamentService = tournamentService;
    }

    public IActionResult Login()
    {
        // If already authenticated, redirect to admin index
        if (IsAuthenticated())
        {
            return RedirectToAction("Index");
        }
        
        return View();
    }

    [HttpPost]
    public IActionResult Login(string passcode)
    {
        if (passcode == AdminPasscode)
        {
            HttpContext.Session.SetString(AdminSessionKey, "true");
            return RedirectToAction("Index");
        }

        TempData["Error"] = "Invalid passcode. Please try again.";
        return View();
    }

    public IActionResult Index()
    {
        if (!IsAuthenticated())
        {
            return RedirectToAction("Login");
        }

        var tournament = _tournamentService.GetTournament();
        return View(tournament);
    }

    [HttpPost]
    public IActionResult UnregisterPlayer(int playerId)
    {
        if (!IsAuthenticated())
        {
            return RedirectToAction("Login");
        }

        var success = _tournamentService.UnregisterPlayer(playerId);
        if (success)
        {
            TempData["Success"] = "Player unregistered successfully.";
        }
        else
        {
            TempData["Error"] = "Failed to unregister player.";
        }

        return RedirectToAction("Index");
    }

    [HttpPost]
    public IActionResult ResetCurrentRound()
    {
        if (!IsAuthenticated())
        {
            return RedirectToAction("Login");
        }

        var success = _tournamentService.ResetCurrentRound();
        if (success)
        {
            TempData["Success"] = "Current round reset successfully.";
        }
        else
        {
            TempData["Error"] = "Failed to reset current round.";
        }

        return RedirectToAction("Index");
    }

    [HttpPost]
    public IActionResult ResetTournament()
    {
        if (!IsAuthenticated())
        {
            return RedirectToAction("Login");
        }

        var success = _tournamentService.ResetTournament();
        if (success)
        {
            TempData["Success"] = "Tournament reset successfully. All players remain registered.";
        }
        else
        {
            TempData["Error"] = "Failed to reset tournament.";
        }

        return RedirectToAction("Index");
    }

    [HttpPost]
    public IActionResult Logout()
    {
        HttpContext.Session.Remove(AdminSessionKey);
        return RedirectToAction("Login");
    }

    private bool IsAuthenticated()
    {
        return HttpContext.Session.GetString(AdminSessionKey) == "true";
    }
}