using Microsoft.AspNetCore.SignalR;

namespace PsrGameServer.Hubs;

public class GameHub : Hub
{
    public async Task JoinTournament(string tournamentId)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, $"Tournament_{tournamentId}");
    }

    public async Task LeaveTournament(string tournamentId)
    {
        await Groups.RemoveFromGroupAsync(Context.ConnectionId, $"Tournament_{tournamentId}");
    }

    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        await base.OnDisconnectedAsync(exception);
    }
}