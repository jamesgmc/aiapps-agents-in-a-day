using Microsoft.EntityFrameworkCore;
using PsrGameServer.Models;

namespace PsrGameServer.Data;

public class GameDbContext : DbContext
{
    public GameDbContext(DbContextOptions<GameDbContext> options) : base(options)
    {
    }

    public DbSet<Player> Players { get; set; }
    public DbSet<Tournament> Tournaments { get; set; }
    public DbSet<Match> Matches { get; set; }
    public DbSet<MatchRound> MatchRounds { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Configure Player entity
        modelBuilder.Entity<Player>(entity =>
        {
            entity.HasKey(p => p.Id);
            entity.Property(p => p.Name).IsRequired().HasMaxLength(50);
            entity.Property(p => p.RegisteredAt).IsRequired();
            entity.Property(p => p.IsActive).IsRequired();
            
            entity.HasOne(p => p.Tournament)
                  .WithMany(t => t.Players)
                  .HasForeignKey(p => p.TournamentId)
                  .OnDelete(DeleteBehavior.Cascade);
        });

        // Configure Tournament entity
        modelBuilder.Entity<Tournament>(entity =>
        {
            entity.HasKey(t => t.Id);
            entity.Property(t => t.Name).HasMaxLength(100);
            entity.Property(t => t.Status).IsRequired();
            entity.Property(t => t.CreatedAt).IsRequired();
            entity.Property(t => t.CurrentRound).IsRequired();
            
            entity.HasOne(t => t.Winner)
                  .WithMany()
                  .HasForeignKey(t => t.WinnerId)
                  .OnDelete(DeleteBehavior.SetNull);
        });

        // Configure Match entity
        modelBuilder.Entity<Match>(entity =>
        {
            entity.HasKey(m => m.Id);
            entity.Property(m => m.Round).IsRequired();
            entity.Property(m => m.Player1Move).IsRequired();
            entity.Property(m => m.Player1MoveSubmittedAt).IsRequired(false);
            entity.Property(m => m.Player2Move).IsRequired();
            entity.Property(m => m.Player2MoveSubmittedAt).IsRequired(false);
            entity.Property(m => m.Status).IsRequired();
            entity.Property(m => m.CreatedAt).IsRequired();
            entity.Property(m => m.CurrentRoundNumber).IsRequired();
            entity.Property(m => m.CurrentRoundStatus).IsRequired();
            
            entity.HasOne(m => m.Tournament)
                  .WithMany(t => t.Matches)
                  .HasForeignKey(m => m.TournamentId)
                  .OnDelete(DeleteBehavior.Cascade);
                  
            entity.HasOne(m => m.Player1)
                  .WithMany()
                  .HasForeignKey(m => m.Player1Id)
                  .OnDelete(DeleteBehavior.SetNull);
                  
            entity.HasOne(m => m.Player2)
                  .WithMany()
                  .HasForeignKey(m => m.Player2Id)
                  .OnDelete(DeleteBehavior.SetNull);
                  
            entity.HasOne(m => m.Winner)
                  .WithMany()
                  .HasForeignKey(m => m.WinnerId)
                  .OnDelete(DeleteBehavior.SetNull);
        });

        // Configure MatchRound entity
        modelBuilder.Entity<MatchRound>(entity =>
        {
            entity.HasKey(mr => mr.Id);
            entity.Property(mr => mr.RoundNumber).IsRequired();
            entity.Property(mr => mr.Player1Move).IsRequired();
            entity.Property(mr => mr.Player1MoveSubmittedAt).IsRequired(false);
            entity.Property(mr => mr.Player2Move).IsRequired();
            entity.Property(mr => mr.Player2MoveSubmittedAt).IsRequired(false);
            entity.Property(mr => mr.Status).IsRequired();
            entity.Property(mr => mr.CreatedAt).IsRequired();
            
            entity.HasOne(mr => mr.Match)
                  .WithMany(m => m.MatchRounds)
                  .HasForeignKey(mr => mr.MatchId)
                  .OnDelete(DeleteBehavior.Cascade);
                  
            entity.HasOne(mr => mr.Winner)
                  .WithMany()
                  .HasForeignKey(mr => mr.WinnerId)
                  .OnDelete(DeleteBehavior.SetNull);
        });
    }
}