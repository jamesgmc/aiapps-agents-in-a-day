using RpsGameServer.Models;

namespace RpsGameServer.Services;

public interface IQuestionService
{
    Task<List<QuestionAnswer>> GetAllQuestionsAsync();
    Task<QuestionAnswer?> GetQuestionByIdAsync(string id);
    Task<QuestionAnswer> GetRandomQuestionAsync();
    Task<QuestionAnswer?> GetQuestionByOrderAsync(int order);
    Task<bool> UpdateQuestionsFromJsonAsync(string jsonContent);
    Task<string> GetQuestionsAsJsonAsync();
    Task<bool> LoadQuestionsFromFileAsync();
}