using ConfigApi.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new() { 
        Title = "Configuration API", 
        Version = "v1",
        Description = "API for retrieving configuration items from Azure Key Vault and configuration files"
    });
});

// Add CORS
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

// Register configuration service
builder.Services.AddScoped<IConfigurationService, ConfigurationService>();

// Add logging
builder.Services.AddLogging();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "Configuration API v1");
        c.RoutePrefix = string.Empty; // Set Swagger UI at the app's root
    });
}

app.UseCors();

app.UseAuthorization();

app.MapControllers();

// Add a default health check endpoint
app.MapGet("/", () => new { 
    status = "running", 
    api = "Configuration API",
    version = "1.0.0",
    endpoints = new {
        health = "/api/configuration/health",
        getConfig = "/api/configuration?key={key}",
        getAllConfigs = "/api/configuration/all",
        swagger = "/swagger"
    }
});

app.Run();
