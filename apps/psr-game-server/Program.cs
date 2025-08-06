using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Models;
using PsrGameServer.Data;
using PsrGameServer.Hubs;
using PsrGameServer.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();

// Configure Entity Framework with In-Memory Database
builder.Services.AddDbContext<GameDbContext>(options =>
    options.UseInMemoryDatabase("PsrGameDb"));

// Add game service
builder.Services.AddScoped<IGameService, GameService>();

// Add SignalR
builder.Services.AddSignalR();

// Add CORS for frontend
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo 
    { 
        Title = "Paper Scissors Rock Game Server API", 
        Version = "v1",
        Description = "REST API for the Paper Scissors Rock tournament game server"
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "PSR Game Server API V1");
        c.RoutePrefix = "swagger";
    });
}

// Serve static files for the frontend
app.UseDefaultFiles();
app.UseStaticFiles();

// Remove HTTPS redirection for development
if (!app.Environment.IsDevelopment())
{
    app.UseHttpsRedirection();
}

app.UseCors("AllowAll");

app.UseAuthorization();

app.MapControllers();
app.MapHub<GameHub>("/gamehub");

app.Run();
